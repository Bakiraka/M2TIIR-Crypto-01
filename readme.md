
 **Cryptographie Avancée : Problème du chèque**
---

Lien dépot Github : https://github.com/Bakiraka/Crypto-01

*Description rapide du problème :*
>Nous avons 3 acteurs : un client, un commerçant, une banque.
Comment faire en sorte qu’une transaction commerciale grave à un chèque puisse être effectuée, en supposant par exemple que ni le client, ni le commerçant ne peuvent contacter la banque pendant l’achat (les deux sont dans un avion), et cela sans qu’aucun acteur ne puisse tricher sur les autres ?
(nous ne traiterons pas du sujet d’un chèque en bois dans ce cas)


##Traitement du problème

Présomption de départ : le client doit avoir sa clé publique signée par la banque (par exemple à son adhésion à la banque)

La transaction se fait de façon active (échange entre les acteurs).

Le chèque contient 4 informations principales :
 - Le chiffrement par le client de la clé publique du commerçant
 - Le chiffrement par la banque de la clé publique du client  
 - La somme de la transaction (en nombre entier)
 - Un numéro unique généré par le commerçant pour vérifier que le chèque ne soit pas copié par un client malveillant

Lors de la fin de la transaction, le commerçant aura le chèque vérifié avec la facture

Quand la banque reçoit le chèque, la banque signera le chèque et le gardera en mémoire afin de pouvoir garantir l’unicité des chèques => un chèque sera viré une et une fois seulement par la banque

----

## Problèmes à résoudre
1. Comment le commerce peut-il être sur que le client est bien de la banque qu’il indique ?

-> Signature de la clé publique du client par la banque, à la présentation du chèque, le commerce donc peut utiliser la clée publique de la banque pour vérifier l’appartenance du client à la banque

2. Comment la banque peut-elle vérifier que le chèque que le commerce lui donne vient bien du client ?

-> La signature du chèque par le client

3. Comment empêcher au commerce de faire une copie du chèque et ensuite la donner à la banque ?

-> Signature du chèque par la banque

4. Comment empêcher la banque d’indiquer au commerce que le chèque a une valeur différente de ce que le commerce en attend ?

-> Cf. 2 : Le client aura vérifié également la somme et signé le chèque

----

## Création d’une preuve de concept

>Langage utilisé : Python (3.4)

5 programmes principaux à créer :

1. Initialisation
  - Génération clé publique/privée banque
  - Génération clé publique/privée client
  - Génération clé publique/privée commerçant
  - Chiffrer la clé publique du client avec la clé privée de la banque :
2. Programme du commerçant
  - Génération d’une facture contenant :
  - Id (UUID par exemple)
  - Somme
  - Information sur le produit
3. Programme du client qui prend en paramètre la facture et va produire le chèque :
  - Clé publique du commerçant chiffrée par le client
  - Clé publique du client chiffrée par la banque
  - Somme de la transaction et numéro unique chiffrés
4. Programme du commerçant : prend facture et le chèque et répond si c’est ok ou pas
  - Vérifie que les données du chèque n’ont pas été altérées par le client
5. Programme de la banque : va prendre chèque et effectue la transaction (ou pas)
  - S’assure que le chèque n’est pas une copie d’un chèque déjà déposé
  - Vérifie que le chèque a bien été chiffré par le client

## Fonctionnement des programmes


1. 1er programme : init.py

- Génération clé publique/privée banque
- Génération clé publique/privée client
- Génération clé publique/privée commerçant
- Chiffrer la clé publique du client avec la clé privée de la banque

Lancement du programme (Exemple) : python3 init.py


2. merchant_generate_invoice.py

  Programme du marchand générant une facture.
  Paramètres :
  - Nom de la facture a générer
  - (optionnel) Nombre de produits à générer
  Sortie : fichier facture généré
  La facture est sous la forme :
  > uniqueid
   produit1 prix1 quantitéproduit1
  > produit2 prix2 quantitéproduit2
  > sommedesprix

**Lancement du programme :**
  ```
  python3.4 merchant_generate_invoice.py <test_invoice> ?numberofproducts?
  ```
  L'unique id généré tente d'utiliser le générateur d'aléatoires fourni par le système d'exploitation.
  La fonction os.urandom() va par exemple chercher dans * /dev/urandom * sur un système unix.

3. 3eme programme : generateCheck.py
           prend 2 parametres : le fichier contenant la facture
                      le fichier qui contiendra le cheque

Programme du client qui prend en paramètre la facture et va produire le chèque :
```  
  Clé publique du commerçant chiffrée par le client
  Clé publique du client chiffrée par la banque
  Somme de la transaction et numéro unique chiffrés
```

**Lancement du programme :**
```
python3.4 generateCheck.py <fileFacture> <fileOutCheck>
```

 4. merchant_verif_invoice_n_check.py
  Programme du marchand vérifiant si un chèque a ou non été modifié.
  Paramètres :
  - fichier facture
  - chèque "signé" par le client
  - clée publique du client
  - clée publique du marchand

  **Sortie :**
 *Sur la sortie standard :* que le chèque est bon ou pas.
 **Lancement du programme :**
 ```
 python3.4 merchant_verif_invoice_n_check.py <test_invoice> <test_check> <clientPk> <commercantPk>
 ```

5. bank_check.py

  Programme de la banque qui va encaisser un chèque.
  Vérifie si un chèque a déjà été encaissé ou non.
  Arguments :
  - fichier chèque
  - clée publique du client
  - clée publique du marchand
  Sortie : Une indication si le chèque a bien été encaissé ou non.
  **Lancement du programme :**
  ```
  python3.4 bank_check.py <test_check> <clientPk> <commercantPk>
  ```

  Fonctionnement :
  La banque va utiliser les 40 premiers caractères de la clée publique du marchand pour faire un fichier d'historique. Elle va ainsi pouvoir vérifier rapidement dans ce fichier, l'existence ou non de l'id unique associé à la clée publique du client.

## Tests
Pour tester le programme, lancer ./testapps.sh $ , avec $ le numéro du script a tester.
Le numéro 6 sert à supprimer les fichiers crées lors de l'utilisation des scripts.
