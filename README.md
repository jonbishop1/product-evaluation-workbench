# Product Evaluation Workbench

Original Python tools and worksheets by Jon Bishop for evaluating developer tools and data products. Connect a buyer task to source evidence, workload costs and an observable result.

The companion product evaluation atlas is being prepared for publication. Existing [marketing skills](https://jonbishop.co/directories/ai-marketing-skills/) cover related research, positioning and evaluation workflows.

## Use the tools

Requires Python 3.10 or later. No dependencies or API credentials are required.

```sh
python -m unittest product_workbench.test_workbench
```

```python
from product_workbench.costs import estimate

# Fictional plan used to demonstrate the arithmetic; not a vendor quote.
plan = dict(base="30", included=20000, overage_per_1000="1.50", rounding="bucket")
result = estimate(plan, monthly_units=22001, peak_daily_units=1000)
assert str(result["total"]) == "34.50"
```

The cost model checks monthly and daily allowances and supports whole-bucket or proportional overage. Choose the rounding policy only when documented or explicitly label it as an assumption. It does not choose the cheapest provider, infer plan compatibility or model omitted taxes and add-ons.

## Keep evidence states separate

```python
from product_workbench.evidence import assess_task

result = assess_task([
    dict(state="observed", evidence="The official documentation names an API-key prerequisite."),
    dict(state="unknown", evidence="No product task has been run."),
])
assert result["execution_verified"] is False
```

Positive observations need evidence. An executed step additionally needs a verified output. Documentation retrieval, file presence and product execution are separate findings. These tools do not generate an agent-readiness score or certify a product.

## Compare source captures

Use `product_workbench.history.snapshot` for content captured through your authorized research tools, then `compare` for two chronological captures of the same URL. Store raw evidence privately. A hash difference means the captured text changed; it does not establish why, or prove that a product or commercial policy changed.

## Worksheets and demonstrations

- [Evaluation workbook](EVALUATION-WORKBOOK.md)
- [Worked synthetic evaluation](examples/synthetic-evaluation.md)
- [Documentation-discovery exercise](examples/documentation-discovery.md)
- [Demonstration script](examples/demo-script.md)
- [Contribution and distribution brief](examples/distribution-brief.md)

The examples distinguish fictional inputs, source observations and tested arithmetic. No vendor software is executed, no messages are sent and no resources are purchased by this package.

## Scope and license

MIT for this original code and these original worksheets. Vendor content and datasets are not included. This repository does not redistribute directory inventories, bulk JSON/CSV exports, private audit traces or credentials. Source research remains linked from the site annotations. Original attribution and third-party rights remain with their respective owners.
