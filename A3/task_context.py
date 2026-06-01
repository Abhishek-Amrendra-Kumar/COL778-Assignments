serve_breakfast_context = {
  "task_idx": 2,
  "task": "serveToast",
  "scene": "FloorPlan16",
  "robot_init_state": {
    'position': {
        'x': 1.25, 
        'y': 0.9037266969680786, 
        'z': 0.0}, 
    'rotation': {
        'x': -0.0, 
        'y': 0.0, 
        'z': 0.0},
    "horizon": 10.0
  },
  "objects_init_state": [
    {
        "objectType": "Toaster",
        "objectName": "Toaster_0fd00d56",
        'position': {
            'x': -1.0070027112960815, 
            'y': 1.0181758403778076, 
            'z': 2.2380008697509766}, 
        'rotation': {
            'x': 0.00027325452538207173, 
            'y': 89.99978637695312, 
            'z': 0.00035513140028342605},
        "property": {}
    },
    {
        "objectType": "CoffeeMachine",
        "objectName": "CoffeeMachine_43b68f52",
        'position': {
            'x': -0.9430000185966492, 
            'y': 1.0181621313095093, 
            'z': 0.6459964513778687}, 
        'rotation': {
            'x': 2.2818327124696225e-05, 
            'y': 89.99988555908203, 
            'z': 7.612370609422214e-06},
        "property": {}
    },
    {
        "objectType": "DiningTable",
        "objectName": "DiningTable_606ac980",
        'position': {
            'x': 2.4193499088287354, 
            'y': 0.003326117992401123, 
            'z': 3.930368661880493}, 
        'rotation': {
            'x': -0.00042156834388151765, 
            'y': 0.10312934219837189, 
            'z': -0.0005923319840803742},
        "property": {}
    },
    {
        "objectType": "Chair",
        "objectName": "Chair_273b67d3",
        'position': {
            'x': 1.6159931421279907, 
            'y': 0.004749655723571777, 
            'z': 4.310997009277344}, 
        'rotation': {
            'x': 359.8515319824219, 
            'y': 107.9744644165039, 
            'z': 0.027935398742556572},
        "property": {}
    },
    {
        "objectType": "Chair",
        "objectName": "Chair_18700f1e",
         'position': {
             'x': 2.7599921226501465, 
             'y': 0.0047490596771240234, 
             'z': 3.086981773376465}, 
        'rotation': {
            'x': 359.8515625, 
            'y': 358.9652404785156, 
            'z': 0.028002042323350906},
        "property": {}
    },
    {
        "objectType": "Plate",
        "objectName": "Plate_de6eacdb",
        "position":{
            'x': 1.9, 
            'y': 0.9037266969680786, 
            'z': 3.9
        },
        "rotation": {
            "x": 0,
            "y": 0,
            "z": 0},
        "property": {}
    },
    
    {
      "objectType": "Knife",
      "objectName": "Knife_a1b750d5",
      "position": {
        'x': -0.5, 
        'y': 1.1037266969680786, 
        'z': 2.0
      },
      "rotation": {
        "x": 0,
        "y": 90,
        "z": 0
      },
      "property": {}
    },
    {
      "objectType": "Bread",
      "objectName": "Bread_17479e9f",
      "position": {
        "x": -0.7,
        "y": 1.0,
        "z": -0.2
      },
      "rotation": {
        "x": 0.00,
        "y": 0.0,
        "z": 0.00
      },
      "property": {}
    },
     {
      "objectType": "Egg",
      "objectName": "Egg_0425ce13",
      "position": {
        "x": -0.7,
        "y": 1.0,
        "z": -0.5
      },
      "rotation": {
        "x": 0.00,
        "y": 0.0,
        "z": 0.00
      },
      "property": {}
    },
    {
        'objectName': 'Pan_e29550a7',
        'objectType': 'Pan',
        "position": {
            'x': 2.5, 
            'y': 1.1037266969680786, 
            'z': -1.5},
        "rotation": {
            "x": 0.00,
            "y": 0.0,
            "z": 0.00
        }
    },
    {
        'objectName': 'Mug_0b3dbbd3',
        'objectType': 'Mug',
        "position": {
            'x': 1.5, 
            'y': 1.1037266969680786, 
            'z': -1.5},
        "rotation": {
            "x": 0.00,
            "y": 0.0,
            "z": 0.00
        }
    }
    
  ],
  'locations':{
        'fridge_l':{
            "position": {
                'x': -0.1, 
                'y': 0.9037266969680786, 
                'z': -0.3},
            "rotation": {
                "x": 0,
                "y": 270,
                "z": 0}
        },
        'counter_2_l':{
            "position": {
                'x': 1.9, 
                'y': 0.9037266969680786, 
                'z': -1.0},
            "rotation": {
                "x": 0,
                "y": 180,
                "z": 0}
        },
        'counter_1_l':{
            "position": {
                'x': 0.0, 
                'y': 0.9037266969680786, 
                'z': 1.4},
            "rotation": {
                "x": 0,
                "y": 270,
                "z": 0
            }
        },
        'dining_table_l':{
            "position": {
                'x': 1.5, 
                'y': 0.9037266969680786, 
                'z': 3.5},
            "rotation": {
                "x": 0,
                "y": 60,
                "z": 0},
        },
    }
}

open_fridge_context = {
  "task_idx": 1,
  "task": "openFridge",
  "scene": "FloorPlan16",
  "robot_init_state": {
    "position": {
        'x': -0.1, 
        'y': 0.9037266969680786, 
        'z': -0.3},
    "rotation": {
        "x": 0,
        "y": 270,
        "z": 0},
    "horizon": 10.0
  },
  "objects_init_state": [
    {
        "objectType": "Toaster",
        "objectName": "Toaster_0fd00d56",
        'position': {
            'x': -1.0070027112960815, 
            'y': 1.0181758403778076, 
            'z': 2.2380008697509766}, 
        'rotation': {
            'x': 0.00027325452538207173, 
            'y': 89.99978637695312, 
            'z': 0.00035513140028342605},
        "property": {}
    },
    {
        "objectType": "CoffeeMachine",
        "objectName": "CoffeeMachine_43b68f52",
        'position': {
            'x': -0.9430000185966492, 
            'y': 1.0181621313095093, 
            'z': 0.6459964513778687}, 
        'rotation': {
            'x': 2.2818327124696225e-05, 
            'y': 89.99988555908203, 
            'z': 7.612370609422214e-06},
        "property": {}
    },
    {
        "objectType": "DiningTable",
        "objectName": "DiningTable_606ac980",
        'position': {
            'x': 2.4193499088287354, 
            'y': 0.003326117992401123, 
            'z': 3.930368661880493}, 
        'rotation': {
            'x': -0.00042156834388151765, 
            'y': 0.10312934219837189, 
            'z': -0.0005923319840803742},
        "property": {}
    },
    {
        "objectType": "Chair",
        "objectName": "Chair_273b67d3",
        'position': {
            'x': 1.6159931421279907, 
            'y': 0.004749655723571777, 
            'z': 4.310997009277344}, 
        'rotation': {
            'x': 359.8515319824219, 
            'y': 107.9744644165039, 
            'z': 0.027935398742556572},
        "property": {}
    },
    {
        "objectType": "Chair",
        "objectName": "Chair_18700f1e",
         'position': {
             'x': 2.7599921226501465, 
             'y': 0.0047490596771240234, 
             'z': 3.086981773376465}, 
        'rotation': {
            'x': 359.8515625, 
            'y': 358.9652404785156, 
            'z': 0.028002042323350906},
        "property": {}
    },
    {
        "objectType": "Plate",
        "objectName": "Plate_de6eacdb",
        "position":{
            'x': 1.9, 
            'y': 0.9037266969680786, 
            'z': 3.9
        },
        "rotation": {
            "x": 0,
            "y": 0,
            "z": 0},
        "property": {}
    },
    
    {
      "objectType": "Knife",
      "objectName": "Knife_a1b750d5",
      "position": {
        'x': -0.5, 
        'y': 1.1037266969680786, 
        'z': 2.0
      },
      "rotation": {
        "x": 0,
        "y": 90,
        "z": 0
      },
      "property": {}
    },
    {
      "objectType": "Bread",
      "objectName": "Bread_17479e9f",
      "position": {
        "x": -0.7,
        "y": 1.0,
        "z": -0.2
      },
      "rotation": {
        "x": 0.00,
        "y": 0.0,
        "z": 0.00
      },
      "property": {}
    },
     {
      "objectType": "Egg",
      "objectName": "Egg_0425ce13",
      "position": {
        "x": -0.7,
        "y": 1.0,
        "z": -0.5
      },
      "rotation": {
        "x": 0.00,
        "y": 0.0,
        "z": 0.00
      },
      "property": {}
    },
    {
        'objectName': 'Pan_e29550a7',
        'objectType': 'Pan',
        "position": {
            'x': 2.5, 
            'y': 1.1037266969680786, 
            'z': -1.5},
        "rotation": {
            "x": 0.00,
            "y": 0.0,
            "z": 0.00
        }
    },
    {
        'objectName': 'Mug_0b3dbbd3',
        'objectType': 'Mug',
        "position": {
            'x': 1.5, 
            'y': 1.1037266969680786, 
            'z': -1.5},
        "rotation": {
            "x": 0.00,
            "y": 0.0,
            "z": 0.00
        }
    }
    
  ],
  'locations':{
        'fridge_l':{
            "position": {
                'x': -0.1, 
                'y': 0.9037266969680786, 
                'z': -0.3},
            "rotation": {
                "x": 0,
                "y": 270,
                "z": 0}
        },
        'counter_2_l':{
            "position": {
                'x': 1.9, 
                'y': 0.9037266969680786, 
                'z': -1.0},
            "rotation": {
                "x": 0,
                "y": 180,
                "z": 0}
        },
        'counter_1_l':{
            "position": {
                'x': 0.0, 
                'y': 0.9037266969680786, 
                'z': 1.4},
            "rotation": {
                "x": 0,
                "y": 270,
                "z": 0
            }
        },
        'dining_table_l':{
            "position": {
                'x': 1.5, 
                'y': 0.9037266969680786, 
                'z': 3.5},
            "rotation": {
                "x": 0,
                "y": 60,
                "z": 0},
        },
    }
}



def get_task_context(name):

    if (name == 'open_fridge'):
        return open_fridge_context
    elif(name == 'serve_toast' or name == 'serve_breakfast'):
        return serve_breakfast_context
    else:
        raise ValueError(f"Invalid task name {name}")