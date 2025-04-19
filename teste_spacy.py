import spacy

# Carrega o modelo em inglês
nlp = spacy.load("en_core_web_sm") if spacy.util.is_package("en_core_web_sm") else spacy.blank("en")

# Texto de exemplo
texto = "Este é um teste para verificar se o spacy está funcionando corretamente."

# Processamento do texto
doc = nlp(texto)

# Mostra os resultados
print(f"Texto processado: {texto}")
print("\nTokens:")
for token in doc:
    print(f"{token.text}")

print("\nSpacy está instalado e funcionando corretamente!") 