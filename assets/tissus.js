/* Les tissus et les zones de chaque modèle.

   Pour ajouter un tissu : une ligne dans la famille voulue, et il apparaît
   dans toutes les zones qui l'acceptent. Les zones extérieures et intérieures
   proposent aussi les tissus mixtes.

   Pour changer un coloris par défaut : le nom du tissu dans "defaut" ci-dessous.
   Un nom inconnu laisse la zone à sa couleur du SVG, sans erreur silencieuse. */
const DONNEES = {
  tissus: {
    exterieur: {
      titre: "Tissus extérieurs",
      liste: [
        { nom: "Ecopak Deep Purple"      , hex: "#4e4482" },
        { nom: "Ecopak Flamingo Pink"    , hex: "#f82d6b" },
        { nom: "Ecopak Fuchsia"          , hex: "#922e75" },
        { nom: "X-Pak Turquoise Green"   , hex: "#048f8c" },
        { nom: "X-Pak Cornflower Blue"   , hex: "#0451b4" },
        { nom: "X-Pak Violet"            , hex: "#31155d" },
        { nom: "X-Pak Cadmium Green"     , hex: "#0d8070" },
        { nom: "X-Pak Goldenrod"         , hex: "#c79b04" },
        { nom: "X-Pak Bluebell"          , hex: "#6c80aa" },
        { nom: "X-Pak Cayenne"           , hex: "#a83c1e" },
        { nom: "X-Pak Alpenglow"         , hex: "#eb936e" },
        { nom: "X-Pak Coyote Brown"      , hex: "#030303" },
        { nom: "X-Pak Evergreen"         , hex: "#568f64" },
        { nom: "X-Pak Fluorescent Orange", hex: "#fb4803" },
        { nom: "X-Pak Coral"             , hex: "#f77861" },
        { nom: "X-Pak Red"               , hex: "#990323" },
      ],
    },
    interieur: {
      titre: "Tissus intérieurs",
      liste: [
        { nom: "Ripstop Gold"           , hex: "#c39941" },
        { nom: "Ripstop White"          , hex: "#ffffff" },
        { nom: "Ripstop Magenta"        , hex: "#e21588" },
        { nom: "Ripstop Red"            , hex: "#dc0d2a" },
        { nom: "Ripstop Orange"         , hex: "#f25b06" },
        { nom: "Ripstop Yellow"         , hex: "#f4c903" },
        { nom: "Ripstop Apple Green"    , hex: "#3fcb0e" },
        { nom: "Ripstop Blue"           , hex: "#0562bc" },
        { nom: "Ripstop Purple"         , hex: "#7f4e88" },
        { nom: "Ripstop Black"          , hex: "#000000" },
        { nom: "Challenge Deep Purple"  , hex: "#3b336e" },
        { nom: "Challenge Lemon Lime"   , hex: "#d1f502" },
        { nom: "Challenge Bright Orange", hex: "#fd3402" },
        { nom: "Challenge Bright Blue"  , hex: "#0160c4" },
        { nom: "Nylon Pink"             , hex: "#cd5994" },
      ],
    },
    mixte: {
      titre: "Tissus mixtes",
      liste: [
        { nom: "Ultragrid Very Berry", hex: "#9e416e" },
        { nom: "Ultragrid Key Lime"  , hex: "#aeb821" },
        { nom: "Ultragrid Tangerine" , hex: "#fb7427" },
        { nom: "Ultragrid Blue Wave" , hex: "#2b6373" },
        { nom: "Ultragrid Moss"      , hex: "#678064" },
        { nom: "Ultragrid Dark Chili", hex: "#8b3b2f" },
        { nom: "Ultragrid Blackout"  , hex: "#000000" },
      ],
    },
    accessoire: {
      titre: "Sangles et zips",
      liste: [
        { nom: "Noir"          , hex: "#000000" },
        { nom: "Nylon Pink"    , hex: "#cd5994" },
        { nom: "Ripstop White" , hex: "#ffffff" },
        { nom: "Ripstop Yellow", hex: "#f4c903" },
      ],
    },
  },

  produits: {
    pouch: [
      { zone: "grande-partie", label: "Grande partie"  , famille: "exterieur" , defaut: "X-Pak Violet" },
      { zone: "petite-partie", label: "Petite partie"  , famille: "exterieur" , defaut: "Ecopak Flamingo Pink" },
      { zone: "chapeau"      , label: "Chapeau (filet)", famille: "interieur" , defaut: "Ultragrid Very Berry" },
      { zone: "sangle-noire" , label: "Sangle"         , famille: "accessoire", defaut: "Noir" },
    ],
    banane: [
      { zone: "face-haut"      , label: "Face avant haut", famille: "exterieur" , defaut: "Ecopak Fuchsia" },
      { zone: "face-bas"       , label: "Face avant bas" , famille: "exterieur" , defaut: "Ecopak Flamingo Pink" },
      { zone: "haut"           , label: "Dessus"         , famille: "exterieur" , defaut: "Ecopak Flamingo Pink" },
      { zone: "dessous"        , label: "Dessous"        , famille: "exterieur" , defaut: "Ecopak Fuchsia" },
      { zone: "ailes"          , label: "Ailes"          , famille: "exterieur" , defaut: "Ecopak Flamingo Pink" },
      { zone: "face-cachee"    , label: "Face arrière"   , famille: "exterieur" , defaut: "X-Pak Coyote Brown" },
      { zone: "zip-haut"       , label: "Zip"            , famille: "accessoire", defaut: "Nylon Pink" },
      { zone: "sangle-ventrale", label: "Sangle ventrale", famille: "accessoire", defaut: "Noir" },
    ],
    portefeuille: [
      { zone: "exterieur-1", label: "Extérieur 1", famille: "exterieur", defaut: "Ecopak Flamingo Pink" },
      { zone: "exterieur-2", label: "Extérieur 2", famille: "exterieur", defaut: "Ecopak Fuchsia" },
      { zone: "interieur"  , label: "Intérieur"  , famille: "interieur", defaut: "Nylon Pink" },
    ],
  },
};
