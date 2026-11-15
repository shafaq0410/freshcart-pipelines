# freshcart-pipelines
Git -> CI -> FreshCart ELT (Snowflake) -> Mage Iris ML pipeline -> RabbitMQ order stream.

- `elt/` FreshCart notebook (Part B)
- `iris_project/` Mage project (Part C)
- `stream/` dispatcher + driver (Part D)
- `tests/` pytest tests run by `.github/workflows/ci.yml`
