import sys
import json

# Test github
class Question:
    def __init__(self, titre, choix, bonne_reponse):
        self.titre = titre
        self.choix = choix
        self.bonne_reponse = bonne_reponse

    def from_json_data(data):
        choix = [i[0] for i in data["choix"]]
        bonne_reponse = [i[0] for i in data["choix"] if i[1] == True]
        if len(bonne_reponse) != 1:
            return None
        q = Question(data["titre"], choix, bonne_reponse[0])
        return q

    def poser(self, num_quest, nb_quest):
        print(f"QUESTION {num_quest} / {nb_quest}")
        print("  " + self.titre)
        for i in range(len(self.choix)):
            print("  ", i+1, "-", self.choix[i])

        print()
        resultat_response_correcte = False
        reponse_int = Question.demander_reponse_numerique_utlisateur(1, len(self.choix))
        if self.choix[reponse_int-1].lower() == self.bonne_reponse.lower():
            print("Bonne réponse")
            resultat_response_correcte = True
        else:
            print("Mauvaise réponse")
            
        print()
        return resultat_response_correcte

    def demander_reponse_numerique_utlisateur(min, max):
        reponse_str = input("Votre réponse (entre " + str(min) + " et " + str(max) + ") : ")
        try:
            reponse_int = int(reponse_str)
            if min <= reponse_int <= max:
                return reponse_int

            print("ERREUR : Vous devez rentrer un nombre entre", min, "et", max)
        except:
            print("ERREUR : Veuillez rentrer uniquement des chiffres")
        return Question.demander_reponse_numerique_utlisateur(min, max)
    
class Questionnaire:
    def __init__(self, questions,categorie, titre, difficulte):
        self.questions = questions
        self.categorie = categorie
        self.titre = titre
        self.difficulte = difficulte

    def from_json_data(data):
        questionnaire_data_questions = data["questions"]
        questions = [Question.from_json_data(i) for i in questionnaire_data_questions]
        return Questionnaire(questions, data["categorie"], data["titre"], data["difficulte"])

    def from_json_file(filename):
        try:
            file = open(filename, "r")
            json_data = file.read()
            file.close()
            questionnaire_data = json.loads(json_data)
            return Questionnaire.from_json_data(questionnaire_data)
        except:
            print("Exception lors de l'ouverture du fichier.")
            return None

    def lancer(self):
        score = 0
        nb_questions = len(self.questions)
        print("---------------")
        print("QUESTIONNAIRE : " + self.titre)
        print("Catégorie : " + self.categorie)
        print("Difficulté : " + self.difficulte)
        print("Nombre de questions : " + str(nb_questions))
        print("---------------")
        
        for i in range (nb_questions):
            question = self.questions[i]
            if question.poser(i+1, nb_questions):
                score += 1
        print("Score final :", score, "sur", len(self.questions))
        return score


# Questionnaire.from_json_file("bandedessinnee_tintin_confirme.json").lancer()
print(sys.argv)

if len(sys.argv) < 2:
    print("ERREUR, vous devez spécifier le nom du fichier json à charger")
    exit(0)

json_filename = sys.argv[1]
questionnaire = Questionnaire.from_json_file(json_filename)
if questionnaire:
    questionnaire.lancer()

