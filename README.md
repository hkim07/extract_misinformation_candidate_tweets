# COVID-19 misinformation about use of antibiotics (for submission to HKS Misinformation Review)

## Data collection (Jan 1 - Mar 31, 2020)
### For replies
twint -s "((corona OR **virus** OR coronavirus OR covid-19 OR covid19 OR 2019-ncov OR wuhanvirus OR (wuhan AND virus)) AND (antibiotic OR antibiotics)) lang:en since:2019-12-31 until:2020-02-01 filter:replies" -o 20191231_20200201_replies.json --json -ho
### For non-replies
twint -s "((corona OR coronavirus OR covid-19 OR covid19 OR 2019-ncov OR wuhanvirus OR (wuhan AND virus)) AND (antibiotic OR antibiotics)) lang:en since:2019-12-31 until:2020-02-01 -filter:replies" -o 20191231_20200201_non_replies.json --json -ho

## Tweet replies preprocessing and sentence-BERT
