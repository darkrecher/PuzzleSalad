
(function () {
  var levelSet =
  {
    "name": "draknek",
    "credits": "<a href='http://www.draknek.org/'>Alan Hazelden</a>",
    "license": "<a href='http://www.wtfpl.net/txt/copying/'>WTFPL</a>",
    "levels": []
  }

  var levels = {}

levels["Formaldehyde"] = {
    "atoms": {
      "1": ["3", "B"],
      "2": ["2", "Dbd"],
      "3": ["1", "f"],
      "4": ["1", "h"]
    },
    "arena": [
"...####",
"...#.3#",
"####..#",
"#..2.1#",
"####..#",
"...#.4#",
"...####"
    ],
    "molecule": [
      "..3",
      "12.",
      "..4"
    ]
  };

levels["Hyponitrous acid"] = {
    "atoms": {
      "1": ["1", "c"],
      "2": ["3", "gd"],
      "3": ["4", "hB"],
      "4": ["4", "Dd"],
      "5": ["3", "hc"],
      "6": ["1", "g"]
    },
    "arena": [
"########",
"#3....1#",
"#..##..#",
"#..52..#",
"#..##..#",
"#6....4#",
"########"
    ],
    "molecule": [
      "12....",
      "..34..",
      "....56"
    ]
  };

levels["Carbonic acid"] = {
    "atoms": {
      "1": ["3", "C"],
      "2": ["1", "d"],
      "3": ["2", "Adf"],
      "4": ["1", "f"],
      "5": ["3", "bh"]
    },
    "arena": [
"#######",
"#2...4#",
"#..3..#",
"#..1..#",
"#5...5#",
"#######"
    ],
    "molecule": [
      "..1..",
      "2.3.4",
      ".5.5."
    ]
  };

levels["Methanol"] = {
    "atoms": {
      "1": ["1", "d"],
      "2": ["1", "e"],
      "3": ["3", "hc"],
      "4": ["2", "aceg"],
      "5": ["1", "g"],
      "6": ["1", "a"]
    },
    "arena": [
"#######",
"#..2..#",
"#..3..#",
"#.5#1.#",
"#..4..#",
"#..6..#",
"#######"
    ],
    "molecule": [
      "1.2.",
      ".345",
      "..6."
    ]
  };

levels["Ethylene"] = {
    "atoms": {
      "1": ["1", "d"],
      "2": ["1", "f"],
      "3": ["2", "Bfh"],
      "4": ["2", "Ddb"],
      "5": ["1", "b"],
      "6": ["1", "h"]
    },
    "arena": [
"#######",
"#1...2#",
"#..3..#",
"#..4..#",
"#5...6#",
"#######"
    ],
    "molecule": [
      "1..2",
      ".34.",
      "5..6"
    ]
  };

levels["Hydrogen Peroxide"] = {
    "atoms": {
      "1": ["1", "d"],
      "2": ["3", "hc"],
      "3": ["3", "gd"],
      "4": ["1", "h"]
    },
    "arena": [
"#######",
"#1...2#",
"#.....#",
"#3...4#",
"#######"
    ],
    "molecule": [
      "1...",
      ".23.",
      "...4"
    ]
  };

levels["Carbon Dioxide"] = {
    "atoms": {
      "1": ["3", "B"],
      "2": ["2", "BD"],
      "3": ["3", "D"]
    },
    "arena": [
"..###..",
"..#.#..",
"###.###",
"#.321.#",
"#######"
    ],
    "molecule": [
      "123"
    ]
  };

levels["Ammonia"] = {
    "atoms": {
      "1": ["1", "e"],
      "2": ["4", "adf"],
      "3": ["1", "b"],
      "4": ["1", "h"]
    },
    "arena": [
"..###..",
".##1##.",
"##...##",
"#4...3#",
"##...##",
".##2##.",
"..###.."
    ],
    "molecule": [
      ".1.",
      ".2.",
      "3.4"
    ]
  };

levels["Methane"] = {
    "atoms": {
      "1": ["1", "d"],
      "2": ["1", "f"],
      "3": ["2", "bdfh"],
      "4": ["1", "b"],
      "5": ["1", "h"]
    },
    "arena": [
"#######",
"#1...2#",
"#.....#",
"#.#3#.#",
"#..#..#",
"#4...5#",
"#######"
    ],
    "molecule": [
      "1.2",
      ".3.",
      "4.5"
    ]
  };

levels["Hydroxylamine"] = {
    "atoms": {
      "1": ["1", "e"],
      "2": ["3", "ae"],
      "3": ["4", "adf"],
      "4": ["1", "b"],
      "5": ["1", "h"]
    },
    "arena": [
"#######",
"#..#..#",
"#..1..#",
"#..3..#",
"#4#2#5#",
"#######"
    ],
    "molecule": [
      ".1.",
      ".2.",
      ".3.",
      "4.5"
    ]
  };

levels["Water"] = {
    "atoms": {
      "1": ["1", "c"],
      "2": ["3", "gd"],
      "3": ["1", "h"]
    },
    "arena": [
"#######",
"#1..###",
"#....##",
"#....##",
"#2..#3#",
"#######"
    ],
    "molecule": [
      "12.",
      "..3"
    ]
  };

levels["Water 2"] = {
    "atoms": {
      "1": ["1", "d"],
      "2": ["3", "hd"],
      "3": ["1", "h"]
    },
    "arena": [
"#######",
"##1..##",
"#.....#",
"#..2..#",
"#....3#",
"##...##",
"#######"
    ],
    "molecule": [
      "1..",
      ".2.",
      "..3"
    ]
  };

levels["Propadiene"] = {
    "atoms": {
      "1": ["1", "e"],
      "2": ["2", "aeB"],
      "3": ["2", "BD"],
      "4": ["2", "Dae"],
      "5": ["1", "a"]
    },
    "arena": [
"#########",
"#.1.#.1.#",
"#...#...#",
"#.4.3.2.#",
"#...#...#",
"#.5.#.5.#",
"#########"
    ],
    "molecule": [
      "1.1",
      "234",
      "5.5"
    ]
  };

levels["Methane 2"] = {
    "atoms": {
      "1": ["1", "d"],
      "2": ["1", "f"],
      "3": ["2", "bdfh"],
      "4": ["1", "b"],
      "5": ["1", "h"]
    },
    "arena": [
"#######",
"#1#.#2#",
"#.....#",
"#..3..#",
"#.....#",
"#4#.#5#",
"#######"
    ],
    "molecule": [
      "1.2",
      ".3.",
      "4.5"
    ]
  };

  function add (name) {
    var level = levels[name];
    level.name = name;
    levelSet.levels.push(level);
    level.id = levelSet.levels.length;
  }

add("Carbon Dioxide");
add("Water");
add("Hydrogen Peroxide");
add("Hydroxylamine");
add("Methane");
add("Water 2");
add("Methanol");
add("Ethylene");
add("Ammonia");
add("Propadiene");
add("Formaldehyde");
add("Hyponitrous acid");
add("Carbonic acid");
add("Methane 2");

  if (typeof(exports) !== 'undefined'){
      exports.levelSet = levelSet;
  }

  if (typeof(KP_ATOMIX) === 'undefined') {
    KP_ATOMIX = {
        levelSets: {}
    }
  }
  KP_ATOMIX.levelSets[levelSet.name] = levelSet;
}());