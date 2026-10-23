"""Testes do resolver.py. Rodar: python3 testes.py"""
import os
import subprocess
import sys
import tempfile
import unittest
from fractions import Fraction as F

PASTA = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PASTA)
import resolver as r  # noqa: E402

# Exemplos do caderno e das atividades (seção 3 da referência).
EX_3_1 = """
max Z = 3x1 + 4x2
2x1 + x2 <= 6
2x1 + 3x2 <= 9
x1, x2 >= 0
resolver: primal
"""
EX_3_2 = """
max Z = 2x1 + 3x2
x1 + 3x2 <= 9
-x1 + 2x2 <= 4
x1 + x2 <= 6
x1, x2 >= 0
resolver: primal
"""
EX_3_3 = """
max Z = 2x1 + x2 + x3
x1 + x2 + x3 <= 50
2x1 + x2 + 2x3 <= 60
3x1 + x2 <= 93
x1, x2, x3 >= 0
resolver: primal
"""
EX_3_4 = """
max Z = 10x1 + 11x2
x1 + 2x2 <= 150
3x1 + 4x2 <= 200
6x1 + x2 <= 175
x1, x2 >= 0
resolver: primal
"""
EX_3_5 = """
max Z = 2x1 + 10x2 + x3
5x1 + 2x2 + x3 <= 15
2x1 + x2 + 7x3 <= 20
x1 + 3x2 + 2x3 <= 25
x1, x2, x3 >= 0
resolver: primal
"""
AT_1 = """
max Z = 3x1 + 2x2
0,5x1 + 0,3x2 <= 3
0,1x1 + 0,2x2 <= 1
0,4x1 + 0,5x2 <= 3
x1, x2 >= 0
resolver: dual
"""
AT_1_DUAL = """
min Z = 3y1 + y2 + 3y3
0,5y1 + 0,1y2 + 0,4y3 >= 3
0,3y1 + 0,2y2 + 0,5y3 >= 2
y1, y2, y3 >= 0
resolver: primal
"""
AT_2 = """
min Z = 5x1 + 2x2 + x3
2x1 + 3x2 + x3 >= 20
6x1 + 8x2 + 5x3 >= 30
7x1 + x2 + 3x3 >= 40
x1 + 2x2 + 4x3 >= 50
x1, x2, x3 >= 0
resolver: dual
"""
AT_2_DUAL = """
max Z = 20y1 + 30y2 + 40y3 + 50y4
2y1 + 6y2 + 7y3 + y4 <= 5
3y1 + 8y2 + y3 + 2y4 <= 2
y1 + 5y2 + 3y3 + 4y4 <= 1
y1, y2, y3, y4 >= 0
resolver: primal
"""
MISTO = """
max Z = x1 + 2x2
x1 + x2 <= 4
x1 - x2 >= 1
x1 + 3x2 = 6
x1, x2 >= 0
resolver: montar_dual
"""


def resolver(texto):
    return r.resolver_problema(r.ler(texto))


class TestLeitura(unittest.TestCase):
    def test_le_objetivo_restricoes_e_modo(self):
        p = r.ler(EX_3_1)
        self.assertEqual(p.sentido, "max")
        self.assertEqual(p.variaveis, ["x1", "x2"])
        self.assertEqual(p.c, [3, 4])
        self.assertEqual(p.A, [[2, 1], [2, 3]])
        self.assertEqual(p.ops, ["<=", "<="])
        self.assertEqual(p.b, [6, 9])
        self.assertEqual(p.modo, "primal")

    def test_le_virgula_decimal_fracao_e_sinal_unicode(self):
        p = r.ler("min Z = 0,5x1 + 1/2x2\n-x1 + 0,25x2 ≥ -3\nx1, x2 ≥ 0\nresolver: primal\n")
        self.assertEqual(p.c, [F(1, 2), F(1, 2)])
        self.assertEqual(p.A, [[-1, F(1, 4)]])
        self.assertEqual(p.ops, [">="])
        self.assertEqual(p.b, [-3])

    def test_variavel_ausente_na_restricao_vale_zero(self):
        p = r.ler(EX_3_3)
        self.assertEqual(p.A[2], [3, 1, 0])

    def test_recusa_ponto(self):
        with self.assertRaisesRegex(r.ErroEntrada, "linha 2"):
            r.ler("max Z = x1\nx1 <= 30.000\nx1 >= 0\nresolver: primal\n")

    def test_recusa_variavel_repetida_na_mesma_linha(self):  # o erro da p02
        with self.assertRaisesRegex(r.ErroEntrada, "x1"):
            r.ler("max Z = 120x1 + 80x2\n2x1 + 1x1 <= 6\nx1, x2 >= 0\nresolver: primal\n")

    def test_recusa_variavel_sem_condicao_de_sinal(self):
        with self.assertRaisesRegex(r.ErroEntrada, "x2"):
            r.ler("max Z = x1 + x2\nx1 + x2 <= 4\nx1 >= 0\nresolver: primal\n")

    def test_recusa_falta_do_modo(self):
        with self.assertRaisesRegex(r.ErroEntrada, "resolver:"):
            r.ler("max Z = x1\nx1 <= 4\nx1 >= 0\n")

    def test_variavel_menor_ou_igual_a_zero_e_caso_nao_coberto(self):
        with self.assertRaisesRegex(r.ErroResolver, "não suportad"):
            r.ler("max Z = x1\nx1 <= 4\nx1 <= 0\nresolver: primal\n")

    def test_recusa_letras_diferentes(self):
        with self.assertRaisesRegex(r.ErroEntrada, "letra"):
            r.ler("max Z = x1 + y2\nx1 + y2 <= 4\nx1, y2 >= 0\nresolver: primal\n")


class TestNumeros(unittest.TestCase):
    def test_valor_com_decimal(self):
        self.assertEqual(r.valor_com_decimal(F(70, 13)), "70/13 ≈ 5,38")
        self.assertEqual(r.valor_com_decimal(F(1, 8)), "1/8 = 0,125")
        self.assertEqual(r.valor_com_decimal(F(51, 4)), "51/4 = 12,75")
        self.assertEqual(r.valor_com_decimal(F(60)), "60")
        self.assertEqual(r.valor_com_decimal(F(-240, 13)), "-240/13 ≈ -18,46")

    def test_conta_de_elemento_com_denominador_comum(self):
        self.assertEqual(r.conta_soma(F(-3), F(4), F(2, 3)),
                         "-3 + 4 × 2/3 = -3 + 8/3 = (-9 + 8)/3 = -1/3")
        self.assertEqual(r.conta_soma(F(1, 2), F(-2, 5), F(3, 5)),
                         "1/2 + (-2/5) × 3/5 = 1/2 - 6/25 = (25 - 12)/50 = 13/50")
        self.assertEqual(r.conta_soma(F(0), F(4), F(1, 3)), "0 + 4 × 1/3 = 4/3")


class TestExemplosDoCaderno(unittest.TestCase):
    def test_3_1_terceiro_quadro_igual_ao_caderno(self):
        q = resolver(EX_3_1).quadros[2].linhas
        self.assertEqual(q["LZ"], [1, F(-1, 3), 0, 0, F(4, 3), 12])
        self.assertEqual(q["L1"], [0, F(4, 3), 0, 1, F(-1, 3), 3])
        self.assertEqual(q["L2"], [0, F(2, 3), 1, 0, F(1, 3), 3])

    def test_3_1_resposta(self):
        res = resolver(EX_3_1)
        self.assertEqual(res.pivos, [("simplex", "x2", "L2"), ("simplex", "x1", "L1")])
        self.assertEqual((res.valores["x1"], res.valores["x2"], res.z), (F(9, 4), F(3, 2), F(51, 4)))

    def test_3_2_continua_enquanto_houver_negativo_na_lz(self):  # o caderno parou em Z = 10,2
        res = resolver(EX_3_2)
        self.assertEqual(res.quadros[2].linhas["L2"], [0, F(-1, 2), 1, 0, F(1, 2), 0, 2])
        self.assertEqual([p[1] for p in res.pivos], ["x2", "x1", "xf2"])
        self.assertEqual((res.valores["x1"], res.valores["x2"], res.z), (F(9, 2), F(3, 2), F(27, 2)))

    def test_3_3_aponta_otimos_multiplos(self):
        res = resolver(EX_3_3)
        self.assertEqual((res.valores["x1"], res.valores["xf1"], res.valores["xf3"], res.z), (30, 20, 3, 60))
        self.assertTrue(res.otimos_multiplos)

    def test_3_4_termina_o_que_o_caderno_nao_fez(self):
        res = resolver(EX_3_4)
        self.assertEqual((res.valores["x1"], res.valores["x2"], res.z), (F(500, 21), F(225, 7), F(1775, 3)))
        self.assertFalse(res.otimos_multiplos)

    def test_3_5_ultima_linha_com_sinais_certos(self):
        res = resolver(EX_3_5)
        self.assertEqual(res.quadros[-1].linhas["L3"], [0, F(-13, 2), 0, F(1, 2), F(-3, 2), 0, 1, F(5, 2)])
        self.assertEqual((res.valores["x2"], res.z), (F(15, 2), 75))


class TestAtividades(unittest.TestCase):
    def test_atividade_1_duas_fases_monta_lw_como_a_atividade(self):
        res = resolver(AT_1_DUAL)
        q1 = res.quadros[0].linhas
        self.assertEqual(q1["LZ"], [-1, 3, 1, 3, 0, 0, 0, 0, 0])
        self.assertEqual(q1["LW"], [0, F(-4, 5), F(-3, 10), F(-9, 10), 1, 1, 0, 0, -5])

    def test_atividade_1_segue_o_mais_negativo_e_chega_ao_otimo(self):
        res = resolver(AT_1_DUAL)
        self.assertEqual(res.pivos, [("fase 1", "y3", "L2"), ("fase 1", "yf2", "L1"), ("fase 2", "y1", "L1")])
        self.assertEqual((res.valores["y1"], res.valores["y3"], res.z), (F(70, 13), F(10, 13), F(240, 13)))

    def test_atividade_2_quadro_final(self):
        res = resolver(AT_2_DUAL)
        self.assertEqual([p[1:] for p in res.pivos], [("y4", "L3"), ("y1", "L2"), ("y3", "L3")])
        self.assertEqual(res.quadros[-1].linhas["LZ"], [1, 0, F(105, 2), 0, 5, 0, F(5, 2), F(25, 2), F(35, 2)])
        self.assertEqual((res.valores["y1"], res.valores["y3"], res.valores["yf1"]), (F(5, 8), F(1, 8), F(23, 8)))

    def test_dual_de_min_le_x_no_quadro_final_do_dual(self):
        rd = r.resolver_pelo_dual(r.ler(AT_2))
        self.assertEqual(rd.x, {"x1": 0, "x2": F(5, 2), "x3": F(25, 2)})
        self.assertEqual(rd.z, F(35, 2))

    def test_dual_de_max_le_x_no_quadro_final_do_dual(self):
        rd = r.resolver_pelo_dual(r.ler(AT_1))
        self.assertEqual(rd.x, {"x1": F(60, 13), "x2": F(30, 13)})
        self.assertEqual(rd.z, F(240, 13))


class TestDual(unittest.TestCase):
    def test_dual_de_max_padrao(self):
        d = r.montar_dual(r.ler(AT_1))
        self.assertEqual(d.sentido, "min")
        self.assertEqual(d.variaveis, ["y1", "y2", "y3"])
        self.assertEqual(d.c, [3, 1, 3])
        self.assertEqual(d.A, [[F(1, 2), F(1, 10), F(2, 5)], [F(3, 10), F(1, 5), F(1, 2)]])
        self.assertEqual(d.ops, [">=", ">="])
        self.assertEqual(d.b, [3, 2])

    def test_dual_de_min_padrao(self):
        d = r.montar_dual(r.ler(AT_2))
        self.assertEqual(d.sentido, "max")
        self.assertEqual(d.c, [20, 30, 40, 50])
        self.assertEqual(d.A, [[2, 6, 7, 1], [3, 8, 1, 2], [1, 5, 3, 4]])
        self.assertEqual(d.ops, ["<=", "<=", "<="])
        self.assertEqual(d.b, [5, 2, 1])

    def test_dual_com_restricoes_mistas_usa_a_tabela_de_sinais(self):
        d = r.montar_dual(r.ler(MISTO))
        self.assertEqual(d.c, [4, 1, 6])
        self.assertEqual(d.A, [[1, 1, 1], [1, -1, 3]])
        self.assertEqual(d.ops, [">=", ">="])
        self.assertEqual(d.b, [1, 2])
        self.assertEqual(d.sinais, [">=0", "<=0", "livre"])

    def test_resolver_pelo_dual_recusa_primal_fora_da_forma_padrao(self):
        with self.assertRaisesRegex(r.ErroResolver, "forma padrão"):
            r.resolver_pelo_dual(r.ler(MISTO))


class TestCasosEspeciais(unittest.TestCase):
    def test_inviavel_quando_a_fase_1_termina_com_w_positivo(self):
        res = resolver("max Z = x1 + x2\nx1 + x2 <= 2\nx1 + x2 >= 4\nx1, x2 >= 0\nresolver: primal\n")
        self.assertEqual(res.status, "inviavel")
        self.assertIsNone(res.z)

    def test_ilimitado_quando_a_coluna_pivo_nao_tem_positivo(self):
        res = resolver("max Z = x1 + x2\nx1 - x2 <= 1\nx1, x2 >= 0\nresolver: primal\n")
        self.assertEqual(res.status, "ilimitado")
        self.assertEqual(res.pivos, [("simplex", "x1", "L1")])

    def test_empate_na_razao_fica_a_linha_de_cima(self):
        res = resolver("max Z = x1\nx1 <= 1\nx1 + x2 <= 1\nx1, x2 >= 0\nresolver: primal\n")
        self.assertEqual(res.pivos[0], ("simplex", "x1", "L1"))
        self.assertTrue(res.degenerado)
        self.assertEqual(res.z, 1)

    def test_empate_na_coluna_fica_a_da_esquerda(self):
        res = resolver("max Z = x1 + x2\nx1 <= 1\nx2 <= 2\nx1, x2 >= 0\nresolver: primal\n")
        self.assertEqual(res.pivos, [("simplex", "x1", "L1"), ("simplex", "x2", "L2")])
        self.assertEqual(res.z, 3)

    def test_restricao_de_igualdade_mistura_de_carnes(self):  # modelo da p01
        res = resolver("min Z = 80x1 + 60x2\n0,20x1 + 0,32x2 <= 0,25\nx1 + x2 = 1\nx1, x2 >= 0\nresolver: primal\n")
        self.assertEqual((res.valores["x1"], res.valores["x2"], res.z), (F(7, 12), F(5, 12), F(215, 3)))

    def test_lado_direito_negativo_vira_maior_ou_igual(self):
        res = resolver("min Z = x1 + x2\n-x1 - x2 <= -2\nx1, x2 >= 0\nresolver: primal\n")
        self.assertIn("LW", res.quadros[0].linhas)
        self.assertEqual(res.z, 2)

    def test_min_so_com_menor_ou_igual_usa_a_linha_menos_z(self):
        res = resolver("min Z = x1 - x2\nx1 + x2 <= 2\nx1, x2 >= 0\nresolver: primal\n")
        self.assertEqual(res.quadros[0].linhas["LZ"][0], -1)
        self.assertEqual((res.valores["x2"], res.z), (2, -2))

    def test_artificial_que_sobra_na_base_sai_por_pivoteamento(self):
        res = resolver("max Z = 4x1 + 2x2\nx1 + 2x2 <= 1\nx1 + x2 >= 1\nx1, x2 >= 0\nresolver: primal\n")
        self.assertEqual(res.pivos, [("fase 1", "x1", "L1"), ("fase 1", "x2", "L2"), ("fase 2", "xf2", "L2")])
        self.assertEqual((res.valores["x1"], res.valores["x2"], res.z), (1, 0, 4))

    def test_restricao_redundante_sai_do_quadro(self):
        res = resolver("max Z = x1\nx1 + x2 = 2\n2x1 + 2x2 = 4\nx1, x2 >= 0\nresolver: primal\n")
        self.assertNotIn("L2", res.quadros[-1].linhas)
        self.assertEqual((res.valores["x1"], res.z), (2, 2))


class TestSaida(unittest.TestCase):
    def rodar(self, texto):
        with tempfile.TemporaryDirectory() as pasta:
            arquivo = os.path.join(pasta, "q.txt")
            with open(arquivo, "w", encoding="utf-8") as f:
                f.write(texto)
            return subprocess.run([sys.executable, os.path.join(PASTA, "resolver.py"), arquivo],
                                  capture_output=True, text=True)

    def test_cli_imprime_a_resposta(self):
        saida = self.rodar(EX_3_1)
        self.assertEqual(saida.returncode, 0, saida.stderr)
        self.assertIn("> **RESPOSTA:** x1 = 9/4 = 2,25; x2 = 3/2 = 1,5; **Z = 51/4 = 12,75**", saida.stdout)

    def test_cli_erro_de_formato_sai_com_codigo_1(self):
        saida = self.rodar("max Z = x1\nx1 <= 30.000\nx1 >= 0\nresolver: primal\n")
        self.assertEqual(saida.returncode, 1)
        self.assertIn("ERRO DE FORMATO", saida.stderr)
        self.assertIn("linha 2", saida.stderr)

    def test_cli_caso_nao_coberto_manda_parar(self):
        saida = self.rodar(MISTO.replace("montar_dual", "dual"))
        self.assertEqual(saida.returncode, 1)
        self.assertIn("CASO NÃO COBERTO", saida.stderr)
        self.assertEqual(saida.stdout, "")

    def test_saida_do_dual_de_min_mostra_o_dual_e_a_resposta_em_x(self):
        texto = r.gerar_saida(r.ler(AT_2))
        self.assertIn("Max Z1 = 20y1 + 30y2 + 40y3 + 50y4", texto)
        self.assertIn("x1 = 0; x2 = 5/2 = 2,5; x3 = 25/2 = 12,5; **Z = 35/2 = 17,5**", texto)

    def test_saida_do_dual_mantem_os_decimais_do_enunciado(self):
        texto = r.gerar_saida(r.ler(AT_1))
        self.assertIn("0,5y1 + 0,1y2 + 0,4y3 ≥ 3", texto)
        self.assertIn("**Z = 240/13 ≈ 18,46**", texto)


if __name__ == "__main__":
    unittest.main(verbosity=1)
