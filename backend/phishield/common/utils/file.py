from typing import BinaryIO, Optional

import vt

from phishield.conf import environment


class FileProcessor:
    def __init__(self):
        self.client = vt.Client(environment.VIRUS_TOTAL_API_KEY)

    async def scan(self, file: BinaryIO) -> Optional[dict]:
        scan = await self.client.scan_file_async(file, wait_for_completion=True)
        analysis = await self.client.get_object_async(f"/analyses/{scan.id}")
        result = analysis.stats
        return result
