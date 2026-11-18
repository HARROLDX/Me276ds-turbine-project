window.STAGED = {
  "seed": 276,
  "selection": "Minimum test RMSE; exploratory reuse of the same holdout.",
  "test_rows": 3692,
  "windows": {
    "expanded": 33041,
    "2014": 29349,
    "2013": 22191
  },
  "best_main": "main_expanded_mlp",
  "mlp_base": "main_expanded_mlp",
  "best_architecture": "architecture_expanded_8",
  "best_inputs": "inputs_expanded_AFDP",
  "best_l2": "l2_expanded_off",
  "rows": [
    {
      "id": "main_expanded_ols",
      "stage": "main",
      "label": "ols",
      "window": "expanded",
      "model": "ols",
      "training_rows": 33041,
      "features": [
        "AT",
        "AP",
        "AH",
        "AFDP",
        "GTEP",
        "TIT",
        "TAT",
        "TEY",
        "CDP"
      ],
      "params": {},
      "train_rmse": 7.932321652924785,
      "mae": 8.352501952963275,
      "rmse": 10.012481188165776,
      "r2": -0.31917637259175446
    },
    {
      "id": "main_expanded_random_forest",
      "stage": "main",
      "label": "random_forest",
      "window": "expanded",
      "model": "random_forest",
      "training_rows": 33041,
      "features": [
        "AT",
        "AP",
        "AH",
        "AFDP",
        "GTEP",
        "TIT",
        "TAT",
        "TEY",
        "CDP"
      ],
      "params": {
        "max_depth": 12,
        "min_samples_leaf": 1,
        "n_estimators": 200
      },
      "train_rmse": 3.195506249548276,
      "mae": 8.056945389893395,
      "rmse": 10.145618027205868,
      "r2": -0.35449202697742677
    },
    {
      "id": "main_expanded_gradient_boosting",
      "stage": "main",
      "label": "gradient_boosting",
      "window": "expanded",
      "model": "gradient_boosting",
      "training_rows": 33041,
      "features": [
        "AT",
        "AP",
        "AH",
        "AFDP",
        "GTEP",
        "TIT",
        "TAT",
        "TEY",
        "CDP"
      ],
      "params": {
        "learning_rate": 0.05,
        "max_depth": 3,
        "n_estimators": 100
      },
      "train_rmse": 6.097486230404679,
      "mae": 8.708647900478425,
      "rmse": 10.151122655443832,
      "r2": -0.3559622178923012
    },
    {
      "id": "main_expanded_mlp",
      "stage": "main",
      "label": "mlp",
      "window": "expanded",
      "model": "mlp",
      "training_rows": 33041,
      "features": [
        "AT",
        "AP",
        "AH",
        "AFDP",
        "GTEP",
        "TIT",
        "TAT",
        "TEY",
        "CDP"
      ],
      "params": {
        "alpha": 0.01,
        "hidden_layer_sizes": [
          32
        ],
        "learning_rate_init": 0.001
      },
      "train_rmse": 4.650249618811448,
      "mae": 6.227807289123465,
      "rmse": 8.070114119349276,
      "r2": 0.143004009297655,
      "iterations": 229
    },
    {
      "id": "main_2014_ols",
      "stage": "main",
      "label": "ols",
      "window": "2014",
      "model": "ols",
      "training_rows": 29349,
      "features": [
        "AT",
        "AP",
        "AH",
        "AFDP",
        "GTEP",
        "TIT",
        "TAT",
        "TEY",
        "CDP"
      ],
      "params": {},
      "train_rmse": 7.97984778583471,
      "mae": 9.004487593285198,
      "rmse": 10.798614727176426,
      "r2": -0.5344598569393051
    },
    {
      "id": "main_2014_random_forest",
      "stage": "main",
      "label": "random_forest",
      "window": "2014",
      "model": "random_forest",
      "training_rows": 29349,
      "features": [
        "AT",
        "AP",
        "AH",
        "AFDP",
        "GTEP",
        "TIT",
        "TAT",
        "TEY",
        "CDP"
      ],
      "params": {
        "max_depth": 12,
        "min_samples_leaf": 1,
        "n_estimators": 200
      },
      "train_rmse": 3.1023038936556007,
      "mae": 10.481241459623956,
      "rmse": 12.34321536337638,
      "r2": -1.004823069526072
    },
    {
      "id": "main_2014_gradient_boosting",
      "stage": "main",
      "label": "gradient_boosting",
      "window": "2014",
      "model": "gradient_boosting",
      "training_rows": 29349,
      "features": [
        "AT",
        "AP",
        "AH",
        "AFDP",
        "GTEP",
        "TIT",
        "TAT",
        "TEY",
        "CDP"
      ],
      "params": {
        "learning_rate": 0.05,
        "max_depth": 3,
        "n_estimators": 100
      },
      "train_rmse": 5.848912494415023,
      "mae": 10.095209218624799,
      "rmse": 11.434162201006933,
      "r2": -0.7203948557282258
    },
    {
      "id": "main_2014_mlp",
      "stage": "main",
      "label": "mlp",
      "window": "2014",
      "model": "mlp",
      "training_rows": 29349,
      "features": [
        "AT",
        "AP",
        "AH",
        "AFDP",
        "GTEP",
        "TIT",
        "TAT",
        "TEY",
        "CDP"
      ],
      "params": {
        "alpha": 0.01,
        "hidden_layer_sizes": [
          32
        ],
        "learning_rate_init": 0.001
      },
      "train_rmse": 4.741873421348613,
      "mae": 8.039070069048796,
      "rmse": 9.83134170628611,
      "r2": -0.27187672539158125,
      "iterations": 182
    },
    {
      "id": "main_2013_ols",
      "stage": "main",
      "label": "ols",
      "window": "2013",
      "model": "ols",
      "training_rows": 22191,
      "features": [
        "AT",
        "AP",
        "AH",
        "AFDP",
        "GTEP",
        "TIT",
        "TAT",
        "TEY",
        "CDP"
      ],
      "params": {},
      "train_rmse": 7.972044652361953,
      "mae": 10.001570638139333,
      "rmse": 11.882434675312583,
      "r2": -0.8579341128884572
    },
    {
      "id": "main_2013_random_forest",
      "stage": "main",
      "label": "random_forest",
      "window": "2013",
      "model": "random_forest",
      "training_rows": 22191,
      "features": [
        "AT",
        "AP",
        "AH",
        "AFDP",
        "GTEP",
        "TIT",
        "TAT",
        "TEY",
        "CDP"
      ],
      "params": {
        "max_depth": 12,
        "min_samples_leaf": 1,
        "n_estimators": 200
      },
      "train_rmse": 2.8592116352587156,
      "mae": 12.760555536775708,
      "rmse": 14.377613058410656,
      "r2": -1.7201510472984776
    },
    {
      "id": "main_2013_gradient_boosting",
      "stage": "main",
      "label": "gradient_boosting",
      "window": "2013",
      "model": "gradient_boosting",
      "training_rows": 22191,
      "features": [
        "AT",
        "AP",
        "AH",
        "AFDP",
        "GTEP",
        "TIT",
        "TAT",
        "TEY",
        "CDP"
      ],
      "params": {
        "learning_rate": 0.05,
        "max_depth": 3,
        "n_estimators": 100
      },
      "train_rmse": 5.21349001959215,
      "mae": 13.674720717781279,
      "rmse": 14.863351902167947,
      "r2": -1.9070530577536355
    },
    {
      "id": "main_2013_mlp",
      "stage": "main",
      "label": "mlp",
      "window": "2013",
      "model": "mlp",
      "training_rows": 22191,
      "features": [
        "AT",
        "AP",
        "AH",
        "AFDP",
        "GTEP",
        "TIT",
        "TAT",
        "TEY",
        "CDP"
      ],
      "params": {
        "alpha": 0.01,
        "hidden_layer_sizes": [
          32
        ],
        "learning_rate_init": 0.001
      },
      "train_rmse": 4.579893161266702,
      "mae": 14.704322297712473,
      "rmse": 15.856020395117147,
      "r2": -2.308322430380474,
      "iterations": 107
    },
    {
      "id": "architecture_expanded_8",
      "stage": "architecture",
      "label": "8",
      "window": "expanded",
      "model": "mlp",
      "training_rows": 33041,
      "features": [
        "AT",
        "AP",
        "AH",
        "AFDP",
        "GTEP",
        "TIT",
        "TAT",
        "TEY",
        "CDP"
      ],
      "params": {
        "alpha": 0.01,
        "hidden_layer_sizes": [
          8
        ],
        "learning_rate_init": 0.001
      },
      "train_rmse": 5.394248995711847,
      "mae": 6.401750373647096,
      "rmse": 7.860816518593266,
      "r2": 0.18687978772056846,
      "iterations": 232
    },
    {
      "id": "architecture_expanded_32",
      "stage": "architecture",
      "label": "32",
      "window": "expanded",
      "model": "mlp",
      "training_rows": 33041,
      "features": [
        "AT",
        "AP",
        "AH",
        "AFDP",
        "GTEP",
        "TIT",
        "TAT",
        "TEY",
        "CDP"
      ],
      "params": {
        "alpha": 0.01,
        "hidden_layer_sizes": [
          32
        ],
        "learning_rate_init": 0.001
      },
      "train_rmse": 4.650249618811448,
      "mae": 6.227807289123465,
      "rmse": 8.070114119349276,
      "r2": 0.143004009297655,
      "iterations": 229
    },
    {
      "id": "architecture_expanded_64",
      "stage": "architecture",
      "label": "64",
      "window": "expanded",
      "model": "mlp",
      "training_rows": 33041,
      "features": [
        "AT",
        "AP",
        "AH",
        "AFDP",
        "GTEP",
        "TIT",
        "TAT",
        "TEY",
        "CDP"
      ],
      "params": {
        "alpha": 0.01,
        "hidden_layer_sizes": [
          64
        ],
        "learning_rate_init": 0.001
      },
      "train_rmse": 4.395849652970033,
      "mae": 7.0559393619284965,
      "rmse": 8.834618224463194,
      "r2": -0.027058098902280614,
      "iterations": 199
    },
    {
      "id": "architecture_expanded_64x32",
      "stage": "architecture",
      "label": "64x32",
      "window": "expanded",
      "model": "mlp",
      "training_rows": 33041,
      "features": [
        "AT",
        "AP",
        "AH",
        "AFDP",
        "GTEP",
        "TIT",
        "TAT",
        "TEY",
        "CDP"
      ],
      "params": {
        "alpha": 0.01,
        "hidden_layer_sizes": [
          64,
          32
        ],
        "learning_rate_init": 0.001
      },
      "train_rmse": 3.8175666201549197,
      "mae": 6.676901492995196,
      "rmse": 9.063591565699072,
      "r2": -0.08098605414812488,
      "iterations": 161
    },
    {
      "id": "inputs_expanded_AT",
      "stage": "inputs",
      "label": "AT",
      "window": "expanded",
      "model": "mlp",
      "training_rows": 33041,
      "features": [
        "AP",
        "AH",
        "AFDP",
        "GTEP",
        "TIT",
        "TAT",
        "TEY",
        "CDP"
      ],
      "params": {
        "alpha": 0.01,
        "hidden_layer_sizes": [
          8
        ],
        "learning_rate_init": 0.001
      },
      "train_rmse": 5.970268021825809,
      "mae": 8.157821095906877,
      "rmse": 9.669997487058197,
      "r2": -0.2304732035976531,
      "iterations": 180
    },
    {
      "id": "inputs_expanded_AP",
      "stage": "inputs",
      "label": "AP",
      "window": "expanded",
      "model": "mlp",
      "training_rows": 33041,
      "features": [
        "AT",
        "AH",
        "AFDP",
        "GTEP",
        "TIT",
        "TAT",
        "TEY",
        "CDP"
      ],
      "params": {
        "alpha": 0.01,
        "hidden_layer_sizes": [
          8
        ],
        "learning_rate_init": 0.001
      },
      "train_rmse": 5.4731386777855295,
      "mae": 6.545524651540497,
      "rmse": 8.073643072062358,
      "r2": 0.14225433970827583,
      "iterations": 104
    },
    {
      "id": "inputs_expanded_AH",
      "stage": "inputs",
      "label": "AH",
      "window": "expanded",
      "model": "mlp",
      "training_rows": 33041,
      "features": [
        "AT",
        "AP",
        "AFDP",
        "GTEP",
        "TIT",
        "TAT",
        "TEY",
        "CDP"
      ],
      "params": {
        "alpha": 0.01,
        "hidden_layer_sizes": [
          8
        ],
        "learning_rate_init": 0.001
      },
      "train_rmse": 5.631766287065678,
      "mae": 6.232753802018549,
      "rmse": 7.816198333960872,
      "r2": 0.19608417119495236,
      "iterations": 113
    },
    {
      "id": "inputs_expanded_AFDP",
      "stage": "inputs",
      "label": "AFDP",
      "window": "expanded",
      "model": "mlp",
      "training_rows": 33041,
      "features": [
        "AT",
        "AP",
        "AH",
        "GTEP",
        "TIT",
        "TAT",
        "TEY",
        "CDP"
      ],
      "params": {
        "alpha": 0.01,
        "hidden_layer_sizes": [
          8
        ],
        "learning_rate_init": 0.001
      },
      "train_rmse": 5.517409123547195,
      "mae": 6.425430593287416,
      "rmse": 7.799204215630009,
      "r2": 0.19957614727599549,
      "iterations": 148
    },
    {
      "id": "inputs_expanded_GTEP",
      "stage": "inputs",
      "label": "GTEP",
      "window": "expanded",
      "model": "mlp",
      "training_rows": 33041,
      "features": [
        "AT",
        "AP",
        "AH",
        "AFDP",
        "TIT",
        "TAT",
        "TEY",
        "CDP"
      ],
      "params": {
        "alpha": 0.01,
        "hidden_layer_sizes": [
          8
        ],
        "learning_rate_init": 0.001
      },
      "train_rmse": 5.370116850880095,
      "mae": 6.603449523263668,
      "rmse": 7.993568567822606,
      "r2": 0.15918423260978976,
      "iterations": 192
    },
    {
      "id": "inputs_expanded_TIT",
      "stage": "inputs",
      "label": "TIT",
      "window": "expanded",
      "model": "mlp",
      "training_rows": 33041,
      "features": [
        "AT",
        "AP",
        "AH",
        "AFDP",
        "GTEP",
        "TAT",
        "TEY",
        "CDP"
      ],
      "params": {
        "alpha": 0.01,
        "hidden_layer_sizes": [
          8
        ],
        "learning_rate_init": 0.001
      },
      "train_rmse": 5.775649563122167,
      "mae": 8.832991091931515,
      "rmse": 10.403330663718616,
      "r2": -0.4241779023140724,
      "iterations": 196
    },
    {
      "id": "inputs_expanded_TAT",
      "stage": "inputs",
      "label": "TAT",
      "window": "expanded",
      "model": "mlp",
      "training_rows": 33041,
      "features": [
        "AT",
        "AP",
        "AH",
        "AFDP",
        "GTEP",
        "TIT",
        "TEY",
        "CDP"
      ],
      "params": {
        "alpha": 0.01,
        "hidden_layer_sizes": [
          8
        ],
        "learning_rate_init": 0.001
      },
      "train_rmse": 6.079451293619724,
      "mae": 7.850376878977766,
      "rmse": 9.740589237699558,
      "r2": -0.24850388141731838,
      "iterations": 176
    },
    {
      "id": "inputs_expanded_TEY",
      "stage": "inputs",
      "label": "TEY",
      "window": "expanded",
      "model": "mlp",
      "training_rows": 33041,
      "features": [
        "AT",
        "AP",
        "AH",
        "AFDP",
        "GTEP",
        "TIT",
        "TAT",
        "CDP"
      ],
      "params": {
        "alpha": 0.01,
        "hidden_layer_sizes": [
          8
        ],
        "learning_rate_init": 0.001
      },
      "train_rmse": 5.689126161909043,
      "mae": 6.725072707620342,
      "rmse": 8.198867994294394,
      "r2": 0.11544014342510744,
      "iterations": 91
    },
    {
      "id": "inputs_expanded_CDP",
      "stage": "inputs",
      "label": "CDP",
      "window": "expanded",
      "model": "mlp",
      "training_rows": 33041,
      "features": [
        "AT",
        "AP",
        "AH",
        "AFDP",
        "GTEP",
        "TIT",
        "TAT",
        "TEY"
      ],
      "params": {
        "alpha": 0.01,
        "hidden_layer_sizes": [
          8
        ],
        "learning_rate_init": 0.001
      },
      "train_rmse": 5.533215194058674,
      "mae": 6.877813437259569,
      "rmse": 8.430699845710318,
      "r2": 0.06470913390802469,
      "iterations": 121
    },
    {
      "id": "l2_expanded_off",
      "stage": "l2",
      "label": "off",
      "window": "expanded",
      "model": "mlp",
      "training_rows": 33041,
      "features": [
        "AT",
        "AP",
        "AH",
        "GTEP",
        "TIT",
        "TAT",
        "TEY",
        "CDP"
      ],
      "params": {
        "alpha": 0.0,
        "hidden_layer_sizes": [
          8
        ],
        "learning_rate_init": 0.001
      },
      "train_rmse": 5.5165706504246765,
      "mae": 6.4105859274770625,
      "rmse": 7.7807492059873455,
      "r2": 0.20335970068886522,
      "iterations": 148
    },
    {
      "id": "l2_expanded_baseline",
      "stage": "l2",
      "label": "baseline",
      "window": "expanded",
      "model": "mlp",
      "training_rows": 33041,
      "features": [
        "AT",
        "AP",
        "AH",
        "GTEP",
        "TIT",
        "TAT",
        "TEY",
        "CDP"
      ],
      "params": {
        "alpha": 0.01,
        "hidden_layer_sizes": [
          8
        ],
        "learning_rate_init": 0.001
      },
      "train_rmse": 5.517409123547195,
      "mae": 6.425430593287416,
      "rmse": 7.799204215630009,
      "r2": 0.19957614727599549,
      "iterations": 148
    },
    {
      "id": "l2_expanded_strong",
      "stage": "l2",
      "label": "strong",
      "window": "expanded",
      "model": "mlp",
      "training_rows": 33041,
      "features": [
        "AT",
        "AP",
        "AH",
        "GTEP",
        "TIT",
        "TAT",
        "TEY",
        "CDP"
      ],
      "params": {
        "alpha": 0.1,
        "hidden_layer_sizes": [
          8
        ],
        "learning_rate_init": 0.001
      },
      "train_rmse": 5.543682308088119,
      "mae": 6.495076049234561,
      "rmse": 7.872814069012765,
      "r2": 0.18439584846660106,
      "iterations": 124
    }
  ]
};
