# covid19_misinformation_analysis

## Data collection
- For replies: twint -s "((corona OR virus OR coronavirus OR covid-19 OR covid19 OR 2019-ncov OR wuhanvirus OR (wuhan AND virus)) AND (antibiotic OR antibiotics)) lang:en until:2020-02-01 since:2019-12-31 filter:replies" -o 20191231_20200201_non_replies.json --json -ho
- For non-replies: twint -s "((corona OR coronavirus OR covid-19 OR covid19 OR 2019-ncov OR wuhanvirus OR (wuhan AND virus)) AND (antibiotic OR antibiotics)) lang:en until:2020-02-01 since:2019-12-31 -filter:replies" -o 20191231_20200201_non_replies.json --json -ho
