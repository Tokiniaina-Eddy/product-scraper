from openai import OpenAI
import json
class TranslatorService:
    def __init__(self, api_key):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        self.model = "tngtech/deepseek-r1t2-chimera:free"

    def traduire_produits(self, products_list):
        if not products_list: return []
        
        prompt = f"""
        Tu es un traducteur expert en e-commerce. 
        Traduis en français les champs 'titre' et 'description' de la liste JSON ci-dessous.
        
        Règles strictes :
        1. Conserve tous les autres champs (id, prix, image, note, lien, avis) intacts.
        2. Retourne uniquement le JSON final valide, sans texte explicatif avant ou après.
        3. Garde le ton professionnel et adapté à la vente en ligne.

        Voici les données : 
        {json.dumps(products_list, indent=2)}
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                # Force la réponse au format JSON (supporté par la plupart des modèles récents)
                response_format={"type": "json_object"}
            )
            
            # Extraction du contenu texte
            content = response.choices[0].message.content
            return json.loads(content)

        except Exception as e:
            print(f"Erreur lors de la traduction OpenRouter : {e}")
            return []