from pydantic_style_schema import SchemaField, model_to_schema
from json_schema_validator import validate_schema
from contrained_token_filer import demonstrate_constrained_decoding
from extraction_pipeline import extraction_with_retry

import run_demo():
    print("Structured Output Pipeline Demo")

    print("1. Schema Defination")
    product_fields = {
        "product": SchemaField(str),
        "price": SchemaField(float, minimum=0),
        "in_stock": SchemaField(bool),
        "categories": SchemaField(list, required=False)
    }
    generated_schema = model_to_schema("Product", product_fields)
    print(json.dumps(generated_schema, indent=2))

    print("2. Schema Validation")
    test_cases = [
        ({"product": "Test", "price": 10.0, "in_stock": True}, "Valid object"),
        ({"product": "Test", "price": -5.0, "in_stock": True}, "Negative price"),
        ({"product": "Test", "in_stock": True}, "Missing price"),
        ({"product": "Test", "price": "ten", "in_stock": True}, "String as price"),
        ("not an object", "String instead of object"),
    ]

    for data, label in test_cases:
        errors = validate_schema(data, product_schema)
        status = "PASS" if not errors else f"FAIL: {errors}"
        print(f"    {label}: {status}")

    print("3. Constrained Decoding")
    demonstrate_constrained_decoding()

    print("4. Extraction Pipeline")
    texts = [
        "The Sony WH-1000XM5 headphones are priced at $348 and currently available.",
        "The new MacBook Pro 16-inch laptop costs $2499 but is sold out.",
        "This is a random sentence with no product info.",
    ]

    for text in texts:
        print(f"\n Input: {text[:60]}...")
        result = extraction_with_retry(text, product_schema)
        if result:
            print(f"    Output: {json.dumps(result)}")
        else:
            print("     Output: FAILED after retries")
