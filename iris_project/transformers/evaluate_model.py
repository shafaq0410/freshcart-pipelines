if 'transformer' not in globals():
    try:
        from mage_ai.data_preparation.decorators import transformer, test
    except ImportError:
        transformer = lambda f: f
        test = lambda f: f
import pandas as pd
from sklearn.metrics import confusion_matrix, classification_report


@transformer
def evaluate(df, *args, **kwargs):
    print(confusion_matrix(df['target'], df['prediction']))
    rep = pd.DataFrame(classification_report(df['target'], df['prediction'], output_dict=True)).T
    print(rep.round(3))
    return rep


@test
def test_report(rep, *args) -> None:
    assert 'accuracy' in rep.index
