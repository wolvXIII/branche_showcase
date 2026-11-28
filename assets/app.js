/* Paiement : prévu dès maintenant, activé une fois l’entreprise immatriculée */
const PAIEMENT = { actif:false, liens:{pouch:"#",banane:"#",portefeuille:"#"}, contact:"https://ig.me/m/branche" };
function renderOrderButtons(){
  document.querySelectorAll("[data-order]").forEach(b=>{
    b.href = PAIEMENT.actif ? PAIEMENT.liens[b.dataset.order] : PAIEMENT.contact;
    b.textContent = PAIEMENT.actif ? "Commander et payer" : "Commander par message";
  });
}



/* Personnalisation : une zone = une variable CSS --zone-<slug> sur l'aperçu.
   Le coloris validé est reporté sur la carte produit. */
/* Les données viennent de assets/tissus.js, chargé avant ce fichier.
   Un <script src> plutôt qu'un fetch() : la page s'ouvre sans serveur. */
function lireDonnees(){
  return typeof DONNEES!=="undefined"?DONNEES:{tissus:{},produits:{}};
}

/* Les pastilles viennent des données plutôt que du HTML : un tissu ajouté à la
   palette apparaît dans toutes les zones de sa famille, sans retouche du balisage.
   Une zone extérieure ou intérieure accepte aussi les tissus mixtes. */
function tissusDe(famille){
  const donnees=lireDonnees();
  const familles=famille==="accessoire"?[famille]:[famille,"mixte"];
  return familles.flatMap(f=>donnees.tissus[f]?.liste||[]);
}

function construirePastilles(donnees){
  Object.entries(donnees.produits).forEach(([produit,zones])=>{
    const panneau=document.getElementById("custo-"+produit);
    if(!panneau) return;
    zones.forEach(({zone,label,famille})=>{
      const hote=panneau.querySelector('[data-zone-row="'+zone+'"] .c-zone__swatches');
      if(!hote) return;
      hote.replaceChildren(...tissusDe(famille).map(({nom,hex})=>{
        const bouton=document.createElement("button");
        bouton.type="button";
        bouton.className="c-tissu";
        bouton.style.setProperty("--tissu",hex);
        Object.assign(bouton.dataset,{zone,color:hex,nom});
        bouton.title=nom;
        bouton.setAttribute("aria-label",nom);
        bouton.setAttribute("aria-pressed","false");
        return bouton;
      }));
      hote.setAttribute("aria-label","Tissu pour "+label);
    });
  });
}

function initPersonnalisation(){
  const donnees=lireDonnees();
  construirePastilles(donnees);

  document.querySelectorAll("[data-personnaliser]").forEach(bouton=>{
    bouton.addEventListener("click",()=>{
      document.getElementById("custo-"+bouton.dataset.personnaliser).showModal();
    });
  });

  document.querySelectorAll(".c-panneau").forEach(panneau=>{
    /* Le <form> couvre tout le panneau, mais un clic sur le fond vise le <dialog>. */
    panneau.addEventListener("click",e=>{ if(e.target===panneau) panneau.close(); });

    const stage=panneau.querySelector("[data-stage]");
    const recap=panneau.querySelector("[data-recap]");
    const defauts=stage.getAttribute("style");
    const choix={};

    const libelle=zone=>panneau.querySelector('[data-zone-row="'+zone+'"] .c-zone__name').textContent;

    const defautDe=zone=>(donnees.produits[panneau.dataset.panneau]||[])
      .find(z=>z.zone===zone)?.defaut;
    const zonesModifiees=()=>Object.entries(choix).filter(([zone,nom])=>nom!==defautDe(zone));

    function majRecap(){
      const modifs=zonesModifiees();
      recap.textContent=modifs.length
        ? modifs.map(([zone,nom])=>libelle(zone)+" : "+nom).join(" · ")
        : "Coloris par défaut.";
    }

    function appliquer(zone,couleur,nom){
      stage.style.setProperty("--zone-"+zone,couleur);
      choix[zone]=nom;
      panneau.querySelector('[data-zone-value="'+zone+'"]').textContent=nom;
      panneau.querySelectorAll('.c-tissu[data-zone="'+zone+'"]').forEach(autre=>
        autre.setAttribute("aria-pressed",String(autre.dataset.nom===nom)));
      majRecap();
    }

    /* Le panneau s'ouvre sur le coloris affiché : les pastilles doivent le refléter. */
    function selectionnerDefauts(){
      (donnees.produits[panneau.dataset.panneau]||[]).forEach(({zone,famille,defaut})=>{
        const tissu=tissusDe(famille).find(t=>t.nom===defaut);
        if(tissu) appliquer(zone,tissu.hex,defaut);
      });
    }

    panneau.querySelectorAll(".c-tissu").forEach(bouton=>bouton.addEventListener("click",()=>{
      const {zone,color,nom}=bouton.dataset;
      appliquer(zone,color,nom);
    }));

    panneau.querySelector("[data-reset]").addEventListener("click",()=>{
      stage.setAttribute("style",defauts);
      selectionnerDefauts();
    });

    panneau.querySelector("[data-valider]").addEventListener("click",()=>{
      const carte=document.querySelector('[data-carte="'+panneau.dataset.panneau+'"]');
      if(carte){
        const apercu=carte.querySelector("[data-apercu]");
        if(apercu) apercu.setAttribute("style",stage.getAttribute("style"));
        const note=carte.querySelector("[data-coloris]");
        const modifs=zonesModifiees();
        if(note) note.textContent=modifs.length
          ? "Coloris : "+modifs.map(([zone,nom])=>libelle(zone)+" en "+nom).join(", ")
          : "Coloris par défaut";
      }
      panneau.close();
    });

    selectionnerDefauts();
  });
}

document.addEventListener("DOMContentLoaded",()=>{
  renderOrderButtons();
  initPersonnalisation();
  document.querySelectorAll("[data-open]").forEach(b=>b.addEventListener("click",()=>document.getElementById(b.dataset.open).showModal()));
  document.querySelectorAll(".c-dialog").forEach(dlg=>{
    dlg.querySelector("[data-close]").addEventListener("click",()=>dlg.close());
    dlg.addEventListener("click",e=>{ if(e.target===dlg) dlg.close(); });
  });
});
