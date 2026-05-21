from flask import Flask, jsonify

app = Flask(__name__)

# Base de données fictive en mémoire
# En vrai chez Adeo, ce serait de vrais serveurs avec de vrais statuts
incidents = [
    {"id": 1, "service": "database", "status": "error", "message": "Connection timeout"},
    {"id": 2, "service": "api-gateway", "status": "error", "message": "High latency detected"},
    {"id": 3, "service": "cache", "status": "ok", "message": "Running fine"},
]


# Route /health — vérifie que l'API tourne
# Chez Adeo : Kubernetes ping cette route pour savoir si le service est vivant
@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "mini-opstomation"})


# Route /incidents — liste tous les incidents et leur état
# Chez Adeo : Opstomation surveille en permanence l'état des serveurs
@app.route("/incidents")
def get_incidents():
    return jsonify(incidents)


# Route /fix/<id> — répare automatiquement un incident
# Chez Adeo : c'est Ansible qui exécute le script de réparation
# ArgoWorkflow déclenche cette étape automatiquement dès qu'une erreur est détectée
@app.route("/fix/<int:incident_id>", methods=["POST"])
def fix_incident(incident_id):
    for incident in incidents:
        if incident["id"] == incident_id:
            if incident["status"] == "error":
                # On simule la réparation automatique
                incident["status"] = "fixed"
                return jsonify({
                    "message": f"Incident {incident_id} fixed automatically",
                    "incident": incident
                })
            # L'incident existe mais n'a pas besoin d'être réparé
            return jsonify({"message": "Incident already ok", "incident": incident})

    # L'incident n'existe pas dans notre système
    return jsonify({"error": "Incident not found"}), 404


if __name__ == "__main__":
    # 0.0.0.0 permet à Docker d'exposer le port vers l'extérieur
    app.run(host="0.0.0.0", port=5000)
    