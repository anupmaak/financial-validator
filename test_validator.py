from main import validation_transaction

def test_validation_transaction_passes():
    row = {
        "date": "2026-01-15",
        "amount": "1500.50",
        "description": "Office supplies",
        "account": "GL-4000"
    }
    errors = validation_transaction(row, line_number=2)
    assert errors == []

def test_validation_transaction_fails():
    row ={
        "date": "2026-01-15",
        "amount": "-200",
        "description": "Refund",
        "account": "GL-4001"
     }
    errors = validation_transaction(row, line_number=2)
    assert errors != []
    assert "Negative" in errors[0]

def test_invalid_date():
    row= {
        "date": "2026-13-15",
        "amount": "1500.50",
        "description": "Office supplies",
        "account": "GL-4000"
    }
    errors = validation_transaction(row, line_number=2)
    assert "Invalid date" in errors[0]

