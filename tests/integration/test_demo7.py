#!/usr/bin/env python
# coding: utf-8

import numpy as np

from sklearn.metrics import roc_auc_score

from lightautoml.automl.presets.tabular_presets import TabularAutoML
from lightautoml.dataset.roles import DatetimeRole


np.random.seed(42)


def test_classic_tabularautoml(sampled_app_train_test, binary_task):

    train, test = sampled_app_train_test

    roles = {
        "target": "TARGET",
        DatetimeRole(base_date=True, seasonality=(), base_feats=False): "report_dt",
    }

    task = binary_task

    automl = TabularAutoML(
        task=task,
        timeout=3600,
        debug=True,
    )
    oof_pred = automl.fit_predict(train, roles=roles, verbose=5)
    test_pred = automl.predict(test)

    not_nan = np.any(~np.isnan(oof_pred.data), axis=1)

    oof_score = roc_auc_score(train[roles["target"]].values[not_nan], oof_pred.data[not_nan][:, 0])
    assert oof_score > 0.7

    test_score = roc_auc_score(test[roles["target"]].values, test_pred.data[:, 0])
    assert test_score > 0.7
