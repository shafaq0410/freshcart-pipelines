if 'data_exporter' not in globals():
    try:
        from mage_ai.data_preparation.decorators import data_exporter, test
    except ImportError:
        data_exporter = lambda f: f
        test = lambda f: f
import os


@data_exporter
def export(df, *args, **kwargs):
    df.to_csv('iris_predictions.csv', index=False)


@test
def test_file(*args) -> None:
    assert os.path.exists('iris_predictions.csv')
