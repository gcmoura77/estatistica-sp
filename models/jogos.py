from pyairtable.orm import Model, fields as F
from config.database import get_secret

class Jogos(Model):
    adversario = F.TextField("Adversário")
    local = F.TextField("Local")
    gols_pro = F.NumberField("Gols Pró")
    gols_contra = F.NumberField("Gols Contra")
    torneio = F.TextField("Torneio")
    data_jogo = F.DatetimeField("Data do Jogo")
    avaliacao = F.RatingField("Avaliação")
    tecnico = F.SelectField("Técnico")
    resultado = F.SelectField("Resultado")
    pontos = F.NumberField("Pontos")

    class Meta:
        base_id = "appt1Ti26Kq8T2LUq"
        table_name = "Jogos"

        @staticmethod
        def api_key():
            return get_secret()

        