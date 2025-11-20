# Web Search Engine System
(Django + Celery + Postgres + OpenSearch + S3 + Redis)

![System Architecture](./docs/architecture.svg)
([diagram](https://viewer.diagrams.net/?tags=%7B%7D&lightbox=1&highlight=0000ff&edit=_blank&layers=1&nav=1&title=Search%20Engine%20Project&dark=auto#R%3Cmxfile%3E%3Cdiagram%20name%3D%22Page-1%22%20id%3D%22dTkWM2QsZdfghEIHy5cy%22%3E7V1dc9q6Fv01zPQ%2BNGP5C3gM0J72TM6c3KYzt%2FfpjMAC3AiL2nJC%2BuuPZEsYWwaMkYCZuA8N3kjG1lpbe2tJlnvOeLX5I4br5V8kQLhnW8Gm50x6tm1bvs%2F%2BcMtbbgHA6eeWRRwGwlYYnsLfSBgtYU3DACWlgpQQTMN12TgjUYRmtGSDcUxey8XmBJd%2FdQ0XSDE8zSBWrf8LA7rMrQPPKuxfULhYyl8GlvhmBWVhYUiWMCCvOybnU88Zx4TQ%2FNNqM0aYt55sl7ze5z3fbi8sRhFtUiH%2BvPz0sHQ%2BTn%2BkU%2FB7OH%2Fs29OPNWcRpoS%2ByTZIXsMVhhE7Gs1JRJ%2FEN4AdQxwuIvZ5xqqjmBleUExD1nz34gtK1sw6W4Y4eIBvJOU%2FklA4e5ZHoyWJw9%2FstBCLc7KvYyqY0AelEk%2B8JjNbzBqjhJV5lFcOKqa%2F4KZU8AEmVBhmBGO4TsJpdhvcsoLxIoxGhFKyEqa8FV4gTkUr9Gwf0%2ByL%2FC%2FasDuO2FXb%2FkLY5d%2Be7QB%2BjjEO%2BcXlZ2INgzY7TSxQ%2BgORFaLxGyuy3CWSLTzntWAdcAQ2W%2FfKD4VvucAVvBecX2xPXdCCfRDMOIEltsqSQ2zaoQ4OM9okNCbPWwfiUM1DjMcEE8aZSUSyQpJLGM1pDZNWYRDg7GRrOAujxXfOrMlHUFgesooTp7B8Ew3KTTGhkMICcwynCD%2BSJKQh4eeP87KjNQkjmrWgN%2Bp5k8wS0zGJ2E3AMLt%2FxLj0ijifxJ3JOwmjJYpDWtDnNNAH%2ByEXGPeBIYid1hCzG1QbQkB6Osp5f1EG1FUB5SbC6s5x1qUuGTdQVANyGcwRc5ixdedxWO0xOwbF8VGkazqEEbtwfL8OP%2FynFdxu%2FzjeQ0N4uzfe8Xu32%2FFPfsJoQQ50%2B3mB%2B8evrVjB%2BnGFFowI5Z7fL3f9jmeKJ17DfsHtuv6zun7X2g%2B6ANkz1ff7rTF%2Bz33%2FEkaMlOMYvuJv6FfKCrYMA85x6IemoO930J8HPQtMNE3MIQ9sU9APOuhbQ%2F%2BEYDxbGkTdWF8%2F7FBvjfojXKAJojDEJh1%2BYCzMd3G%2BPfbfl%2BxnKUbmgLeBKeCBpQJ%2FU4M9376zvZsd7yUofgln6JDOl2UCslgbtS9vAZUidmnY50s5QPYVfcsUZWqE4YPc6gZ%2BOgd%2BdgnmHXLoB7qxtqsC%2FZ6jQpJOVyHNHP9DGmONUaGMPbBMgt9Y9e3A3wV%2FgeifZCqGfj%2FJ9GtgDn%2FHJP63rgLf8PTf8awgHySelRbUSMFg4B7MCXzLWE7QVAsGnRisPSfYwm56IhA0HSXWoPyeY0KSS0K%2FUhS%2FaYsGVdSBuTFijRLchQJdoYArR7oDge0eHhy65gJBU%2BlYkqoLBBoHhxJ244GgqVRcg%2FJ7DgRscLArFPMVgjrHBxX4zUUE%2B9ZVQ7d%2F5%2B%2F%2B699sgHgl8TNrgQMCIsIsbcjUBF6uBVXsYbk11KVFtueX4gXou%2BVFJK4%2FMEWlpmqi3amJ%2BgOGxF3CrLiNIdCbKos1oL%2Fn%2BDHjvQCPIFxX5Ke0rQCt6VJfCKkQYnApQjRVGztClAgxR5QNLLWKzBUGAHApCtQIjh0FjlOA3XoMZ%2FQhjJ6TD0u6MkiFangwtbDUbqomdlQoUYG1V4Luo2CMEYwMc6F%2FKS401Rw7LpQ1R0pi9A2%2BmqWBbV2KBk1Xo3Y0UGnwyPuF4EPWPWiUG6pccC7FhaYaY8eFEhfCKECbCZmlK9Zsxtng14oO%2BslQI0XelBTlD66lPcUkZYgH4sw1jCgrUd9QECYHhKjs%2BxH3m3YyFHBqnmH0xMBPnsatPL0EBvadXIqi%2F8HGGhnzIMm6jiTrSChMnv%2BborTdhFXdXKakgVyoYEptdBqrjSrindp47jqFCspDYyjXyIu3FROs24gJsgkeMmpnpgWGSdJrOHkRcBbC5OD0Nknogl3rpB2NgF%2FDI7e8zAnYoLxc3rGMMaupTikp2EUMoUwsUKItWrjllS%2BSIvrRbipJdmir0xR%2FkqkxxIfGEG%2BqPNYg3uUH5%2BYHFZSBbQzmGlGxSxCaJQhHk4IpJtN%2FuO7Et886sATaGaWzZ9RyC6SatGC7Z8q%2BtMADxvjUVJ2UxOsCRRYoWJz4Qlf47%2BlPNKPaosWWCMbzg6ZCZAe7Ok8VsBqUNZth8M2lCk3XQNaA36UKZ690rW6FYQpmt0YjvK1U4Wr68nbXyhZic%2F5IxD%2FZlMSBJOHvNYryZ6XGOE1oW%2BXZr1GeBxXluZot9I1lC25TEdLt5q8UEeFrzhhN48rBhXRnv%2FFeaR3kCuR5B2AKc2MqtFyN3wbzLkE4%2B5nIMsrANgaz%2BCEUKLtFqxkDSeMZOnAyNbOYpfFLMRzncf%2Beb11dwI%2BiQFrIOvNRtAnpD1GDf%2F4%2FR%2B7Oy8qyO%2F4hgMwOiu%2BKAG4p%2BARoDlNc4MMuY4EOUlpx5i%2Ffvz8yS5xvh5fUgxojDGn4Um7HOsSyquy24dtOAcHAKqDb85%2BBsasRY%2FXZ2DMwtu6GQ7%2BEMwD2SUjzmpPN7sHbzsEj80vWejxxzW2sBWR2y9x7SRYkgvhTYW3KEJld7VAkk417PJMfZe3Dt1A4kyfnebanEXVfHQVeybUPAK4NXNX%2Fk20Qvxqc%2Fq068VloasOsr2CWvQCBP2KSPa54Vez6OoOsOnejFbzG7rYHZHvLgKJedqTdT%2BUs1q6fwheO%2BU8y1RGiV5tHHpRLw%2Bzq9tSVYXZ%2B0aKagVA%2B0MkkNXPXxiTHPjdUt6VXQ%2FLIJVI75EHRr3xZmCVjOV8qdhkiDat6jWkiDXUSyWA8YRd6hAwVll2i53HV9O8Zvb2SOOCtcPVcQXZKesBVN0G4VrJwkaDiKNBiAoOeeKGSbTGIIF85dlWAgU6A1cWiFwHYuUZuL6ezVHhZl8%2BwyCf3etlrt6h4xdHVUD5FmzkPPAkRuI3%2BtSY4mwnD1Z0ivOpMXO49ShhWz%2BRb1p1lld9xY4MhFzis7b%2FKa6wMx3hPp%2B4jn3G%2FHNGkRlTqUAau2y6VNB431I4le3pN9ixCF5L9iwkye%2F0ymZUNE%2FeQWRvfdCpO8inq8%2Fi2h1J33BW10Crj8p0F%2FEpsK2TMfcTjR8b0yZoEVUxWWyRm%2F6VrlsIgHTTcL2PvY6lXYanY52tvz1qt0PftCnvza9jXMTvl6oPqmprGXfx23zl5IRce%2FHs6JUBbj4ykKXHY65gWAKc7pkGBSTqO5tFAO1fyK%2B%2FJ9ARD9icplQqO0JNaulLfqUxLGg4wvk4dVdUsynwtmPNAsklnTsSfiNI3sXQJppQwE9%2BhoFeMe9QxUK5YNdBRGfn7lTDiDMyEkZKr17l18Dnk2JyiqDlacvRTncCvRAdXDGf3%2BUC1vHNaNAFVD6q%2BqMJwDJBrfMRbocXKht72jblHl2v4qpzD6fLA10WU2Xx06d92bUa2AG%2FvsppJr2Z1TP7uGWZ7ergXXx5fNVHLJFGFec9gaJewaZ5ByyJkPk%2FQibixw%2BJV13nx4o3hzqd%2FAQ%3D%3D%3C%2Fdiagram%3E%3C%2Fmxfile%3E))

A scalable web search engine featuring:

- Distributed crawling (with **1-hour SLA**)
- Link extraction & recursive crawling
- Raw + parsed content Blob storage in S3
- OpenSearch indexing (AWS ElasticSearch)
- Keyword search API
- Page Details API
- Scalable infrastructure (multiple api instances, workers, db clustering)


---

## 🗂 Repository Structure

```text

├─ requirements.txt            # Django, Celery, Redis, OpenSearch, boto3, etc.
├─ env.example                 # Environment template

├─ app/                        # Django project configuration
│  ├─ settings.py
│  └─ urls.py

├─ api/                        # HTTP layer (controllers)
│  ├─ views.py                 # /crawl, /crawl/{job_id}, /search, /pages/{id}
│  └─ throttling.py            # SLA-aware throttling (overload protection)

├─ services/                   # Business logic
│  ├─ crawl_service.py         # submitCrawl(), getJobStatus()
│  ├─ search_service.py        # OpenSearch query pipeline
│  └─ page_service.py          # Page metadata (Postgres) + content (S3)

├─ crawler/                    # Distributed crawler (Celery workers)
│  ├─ tasks.py                 # crawlPage(url, depth, root_job_id)
│  ├─ link_filter.py           # Depth limiting, dedupe, domain filtering
│  └─ models.py                # CrawlJob (Crawl job tree + SLA fields), Page (Metadata for each crawled page) models

├─ integrations/               # External system adapters
│  ├─ opensearch_client.py     # OpenSearch adapter
│  ├─ s3_client.py             # S3 adapter
