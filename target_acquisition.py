import asyncio
import aiohttp
from bs4 import BeautifulSoup
import aiodns
import ipaddress

class TargetAcquisition:
    def __init__(self):
        self.resolver = aiodns.DNSResolver()

    async def acquire_targets(self, initial_target: str, options: dict) -> dict:
        targets = {
            'domains': set(),
            'ips': set(),
            'urls': set(),
            'subdomains': set(),
            'related_companies': set(),
            'cloud_assets': set(),
        }

        targets['domains'].add(initial_target)

        if options.get('passive_discovery', True):
            await self.passive_discovery(initial_target, targets)

        if options.get('active_discovery', True):
            await self.active_discovery(initial_target, targets)

        if options.get('subdomain_enumeration', True):
            await self.enumerate_subdomains(initial_target, targets)

        if options.get('related_company_discovery', True):
            await self.discover_related_companies(initial_target, targets)

        if options.get('cloud_asset_discovery', True):
            await self.discover_cloud_assets(initial_target, targets)

        return {k: list(v) for k, v in targets.items()}

    async def passive_discovery(self, target: str, targets: dict):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://crt.sh/?q=%25.{target}&output=json") as response:
                if response.status == 200:
                    data = await response.json()
                    for entry in data:
                        domain = entry['name_value'].lower()
                        if domain.endswith(target):
                            targets['domains'].add(domain)

    async def active_discovery(self, target: str, targets: dict):
        try:
            ip_address = await self.resolver.query(target, 'A')
            if ip_address:
                targets['ips'].add(ip_address[0].host)

            ptr_records = await self.resolver.query(ip_address[0].host, 'PTR')
            if ptr_records:
                targets['domains'].add(ptr_records[0].host)
        except aiodns.error.DNSError:
            pass

    async def enumerate_subdomains(self, target: str, targets: dict):
        common_subdomains = ['www', 'mail', 'ftp', 'blog', 'shop', 'dev']
        tasks = [self.resolver.query(f"{subdomain}.{target}", 'A') for subdomain in common_subdomains]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for subdomain, result in zip(common_subdomains, results):
            if not isinstance(result, Exception) and result:
                full_domain = f"{subdomain}.{target}"
                targets['subdomains'].add(full_domain)
                targets['ips'].add(result[0].host)

    async def discover_related_companies(self, target: str, targets: dict):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.crunchbase.com/v3.1/organizations?query={target}") as response:
                if response.status == 200:
                    data = await response.json()
                    for item in data.get('data', {}).get('items', []):
                        targets['related_companies'].add(item['properties']['name'])

    async def discover_cloud_assets(self, target: str, targets: dict):
        cloud_providers = ['s3.amazonaws.com', 'blob.core.windows.net', 'storage.googleapis.com']
        for provider in cloud_providers:
            asset = f"{target.replace('.', '-')}.{provider}"
            try:
                await self.resolver.query(asset, 'CNAME')
                targets['cloud_assets'].add(asset)
            except aiodns.error.DNSError:
                pass

target_acquisition = TargetAcquisition()
