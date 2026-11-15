if 'transformer' not in globals():
    try:
        from mage_ai.data_preparation.decorators import transformer, test
    except ImportError:          # running under pytest / CI, outside Mage
        transformer = lambda f: f
        test = lambda f: f
from sklearn.model_selection import train_test_split


@transformer
def transform(df, *args, **kwargs):
    train_idx, test_idx = train_test_split(df.index, test_size=0.3, random_state=42, stratify=df['target'])
    out = df.copy()
    out['split'] = 'train'
    out.loc[test_idx, 'split'] = 'test'
    return out


@test
def test_output(df, *args) -> None:
    assert set(df['split']) == {'train', 'test'}
    assert (df['split'] == 'test').sum() == 30
