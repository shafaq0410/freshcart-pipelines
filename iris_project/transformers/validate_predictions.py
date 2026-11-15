
if 'transformer' not in globals():
    try:
        from mage_ai.data_preparation.decorators import transformer, test
    except ImportError:
        transformer = lambda f: f
        test = lambda f: f


@transformer
def validate_predictions(df, *args, **kwargs):
    """
    Validate that model predictions contain valid Iris class labels.
    """
    valid_classes = {0, 1, 2}

    assert 'prediction' in df.columns, "Missing prediction column"

    predictions = set(df['prediction'].dropna().unique())

    assert predictions.issubset(valid_classes), (
        f"Invalid prediction classes found: {predictions}"
    )

    print("Custom validation passed: all predictions are valid.")

    return df


@test
def test_predictions(df, *args):
    assert 'prediction' in df.columns
    assert df['prediction'].notna().all()
