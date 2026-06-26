import hashlib
import scrapy


class CleanPipeline:
    def process_item(self, item, spider):
        for field in item.fields:
            val = item.get(field)
            if val and isinstance(val, str):
                item[field] = val.strip()
        return item


class DedupPipeline:
    seen = set()

    def process_item(self, item, spider):
        fingerprint = hashlib.md5(
            f"{item.get('title', '')}{item.get('company', '')}{item.get('url', '')}".encode()
        ).hexdigest()
        if fingerprint in self.seen:
            raise scrapy.exceptions.DropItem(f"Duplicate: {item.get('title')}")
        self.seen.add(fingerprint)
        return item
