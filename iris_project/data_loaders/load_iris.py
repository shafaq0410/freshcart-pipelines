if 'data_loader' not in globals():
    try:
        from mage_ai.data_preparation.decorators import data_loader, test
    except ImportError:
        data_loader = lambda f: f
        test = lambda f: f
from sklearn.datasets import load_iris as _load_iris


@data_loader
def load_data(*args, **kwargs):
    return _load_iris(as_frame=True).frame


@test
def test_output(df, *args) -> None:
    assert df is not None and len(df) == 150, 'expected 150 rows'
    assert df['target'].nunique() == 3, 'expected 3 classes'
