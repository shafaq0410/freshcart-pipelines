if 'transformer' not in globals():
    try:
        from mage_ai.data_preparation.decorators import transformer, test
    except ImportError:
        transformer = lambda f: f
        test = lambda f: f
from sklearn.tree import DecisionTreeClassifier

MIN_ACCURACY = 0.90


@transformer
def train(df, *args, **kwargs):
    max_depth = int(kwargs.get('max_depth', 3))      # --runtime-vars '{"max_depth": 2}'
    feats = [c for c in df.columns if c not in ('target', 'split')]
    tr, te = df[df['split'] == 'train'], df[df['split'] == 'test'].copy()
    model = DecisionTreeClassifier(max_depth=max_depth, random_state=42).fit(tr[feats], tr['target'])
    te['prediction'] = model.predict(te[feats])
    print(f'max_depth={max_depth} test accuracy={(te.target == te.prediction).mean():.3f}')
    return te


@test
def test_accuracy(df, *args) -> None:
    acc = (df['target'] == df['prediction']).mean()
    assert acc >= MIN_ACCURACY, f'accuracy {acc:.3f} is below {MIN_ACCURACY}'
