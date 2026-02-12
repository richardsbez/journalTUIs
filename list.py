import os
import json
from datetime import datetime, timedelta
from collections import defaultdict
import re
import calendar

ARQUIVO_DADOS = "journal_data.json"


# Cores ANSI
class Cor:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"

    # Cores básicas
    PRETO = "\033[30m"
    VERMELHO = "\033[31m"
    VERDE = "\033[32m"
    AMARELO = "\033[33m"
    AZUL = "\033[34m"
    MAGENTA = "\033[35m"
    CIANO = "\033[36m"
    BRANCO = "\033[37m"

    # Cores brilhantes
    VERMELHO_B = "\033[91m"
    VERDE_B = "\033[92m"
    AMARELO_B = "\033[93m"
    AZUL_B = "\033[94m"
    MAGENTA_B = "\033[95m"
    CIANO_B = "\033[96m"

    # Backgrounds
    BG_VERMELHO = "\033[41m"
    BG_VERDE = "\033[42m"
    BG_AMARELO = "\033[43m"
    BG_AZUL = "\033[44m"
    BG_CINZA = "\033[100m"


# ============== UTILIDADES ==============
def len_visual(texto):
    """Calcula comprimento visual ignorando códigos ANSI"""
    return len(re.sub(r"\033\[[0-9;]+m", "", texto))


# ============== PERSISTÊNCIA DE DADOS ==============
def carregar_dados():
    """Carrega dados salvos do arquivo JSON"""
    if os.path.exists(ARQUIVO_DADOS):
        try:
            with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
                dados = json.load(f)
                # Migrar tarefas antigas para o novo formato com múltiplos cadernos
                for tarefa in dados.get("tarefas", []):
                    if "cadernos" not in tarefa:
                        tarefa["cadernos"] = [tarefa["caderno"]]

                # Inicializar calendário se não existir
                if "calendario" not in dados:
                    dados["calendario"] = {}

                # Inicializar atividades diárias se não existir
                if "atividades_diarias" not in dados:
                    dados["atividades_diarias"] = {}

                return dados
        except:
            pass

    # Obter mês e semana atual
    agora = datetime.now()
    mes_atual = agora.strftime("%B")
    # Traduzir mês para português
    meses_pt = {
        "January": "Janeiro",
        "February": "Fevereiro",
        "March": "Março",
        "April": "Abril",
        "May": "Maio",
        "June": "Junho",
        "July": "Julho",
        "August": "Agosto",
        "September": "Setembro",
        "October": "Outubro",
        "November": "Novembro",
        "December": "Dezembro",
    }
    mes_atual = meses_pt.get(mes_atual, mes_atual)

    # Calcular semana do mês
    dia_mes = agora.day
    semana_mes = ((dia_mes - 1) // 7) + 1

    return {
        "cadernos": ["Hoje", "Faculdade", "Trabalho", "Projetos"],
        "caderno_ativo": "Hoje",
        "tarefas": [
            {
                "id": 1,
                "texto": "Estudar cálculo",
                "status": "•",
                "caderno": "Faculdade",
                "cadernos": ["Faculdade"],
                "prioridade": 2,
            },
            {
                "id": 2,
                "texto": "Beber água",
                "status": "X",
                "caderno": "Hoje",
                "cadernos": ["Hoje"],
                "prioridade": 1,
            },
            {
                "id": 3,
                "texto": "Revisar código",
                "status": "•",
                "caderno": "Trabalho",
                "cadernos": ["Trabalho"],
                "prioridade": 3,
            },
        ],
        "metas": {
            "semanais": [
                {
                    "texto": f"{mes_atual} - Semana {semana_mes}",
                    "progresso": 0,
                    "tipo": "semana_atual",
                },
                {"texto": "Estudar 10h", "progresso": 60},
                {"texto": "Ler 1 livro", "progresso": 30},
            ],
            "mensais": [
                {"texto": "Janeiro - 31 dias", "progresso": 0, "dias_total": 31},
                {"texto": "Fevereiro - 28/29 dias", "progresso": 0, "dias_total": 29},
                {"texto": "Março - 31 dias", "progresso": 0, "dias_total": 31},
                {"texto": "Abril - 30 dias", "progresso": 0, "dias_total": 30},
                {"texto": "Maio - 31 dias", "progresso": 0, "dias_total": 31},
                {"texto": "Junho - 30 dias", "progresso": 0, "dias_total": 30},
                {"texto": "Julho - 31 dias", "progresso": 0, "dias_total": 31},
                {"texto": "Agosto - 31 dias", "progresso": 0, "dias_total": 31},
                {"texto": "Setembro - 30 dias", "progresso": 0, "dias_total": 30},
                {"texto": "Outubro - 31 dias", "progresso": 0, "dias_total": 31},
                {"texto": "Novembro - 30 dias", "progresso": 0, "dias_total": 30},
                {"texto": "Dezembro - 31 dias", "progresso": 0, "dias_total": 31},
            ],
            "anuais": [
                {"texto": "Concluir graduação", "progresso": 80},
                {"texto": "Aprender Python", "progresso": 65},
            ],
        },
        "notas": {},
        "calendario": {},
        "atividades_diarias": {},
        "proximo_id": 4,
    }


def salvar_dados(dados):
    """Salva dados no arquivo JSON"""
    try:
        with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"{Cor.VERMELHO}✗ Erro ao salvar: {e}{Cor.RESET}")
        return False


# ============== CALENDÁRIO ==============
def criar_calendario_mensal(ano, mes, dias_marcados=None):
    """Cria um calendário visual colorido para um mês"""
    if dias_marcados is None:
        dias_marcados = {}

    # Configurar calendário para começar na segunda-feira
    cal = calendar.monthcalendar(ano, mes)

    # Nomes dos dias da semana em português
    dias_semana = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]

    # Meses em português
    meses_pt = [
        "Janeiro",
        "Fevereiro",
        "Março",
        "Abril",
        "Maio",
        "Junho",
        "Julho",
        "Agosto",
        "Setembro",
        "Outubro",
        "Novembro",
        "Dezembro",
    ]

    linhas = []

    # Cabeçalho do mês
    linhas.append(f"{Cor.BOLD}{Cor.CIANO_B}{meses_pt[mes - 1]} {ano}{Cor.RESET}")
    linhas.append(f"{Cor.DIM}{'─' * 42}{Cor.RESET}")

    # Dias da semana
    header = "  ".join(f"{Cor.BOLD}{d:^3}{Cor.RESET}" for d in dias_semana)
    linhas.append(header)
    linhas.append(f"{Cor.DIM}{'─' * 42}{Cor.RESET}")

    # Dias do mês
    dia_hoje = (
        datetime.now().day
        if (datetime.now().year == ano and datetime.now().month == mes)
        else -1
    )

    for semana in cal:
        linha_dias = []
        for dia in semana:
            if dia == 0:
                linha_dias.append(f"{Cor.DIM}   {Cor.RESET}")
            else:
                # Verificar status do dia
                status = dias_marcados.get(dia, None)

                # Colorir baseado no status
                if dia == dia_hoje:
                    # Dia atual em destaque
                    dia_str = f"{Cor.BG_AZUL}{Cor.BRANCO}{dia:2d}{Cor.RESET} "
                elif status == "completo":
                    # Dia completado
                    dia_str = f"{Cor.VERDE_B}{dia:2d}{Cor.RESET} "
                elif status == "parcial":
                    # Dia com progresso parcial
                    dia_str = f"{Cor.AMARELO_B}{dia:2d}{Cor.RESET} "
                elif status == "falha":
                    # Dia sem progresso
                    dia_str = f"{Cor.VERMELHO_B}{dia:2d}{Cor.RESET} "
                else:
                    # Dia sem dados
                    dia_str = f"{Cor.DIM}{dia:2d}{Cor.RESET} "

                linha_dias.append(dia_str)

        linhas.append("  ".join(linha_dias))

    # Legenda
    linhas.append(f"\n{Cor.DIM}{'─' * 42}{Cor.RESET}")
    linhas.append(
        f"{Cor.VERDE_B}██{Cor.RESET} Completo  {Cor.AMARELO_B}██{Cor.RESET} Parcial  {Cor.VERMELHO_B}██{Cor.RESET} Pendente  {Cor.BG_AZUL}{Cor.BRANCO}██{Cor.RESET} Hoje"
    )

    return "\n".join(linhas)


def marcar_dia_calendario(dados, status="completo"):
    """Marca o dia atual no calendário com um status"""
    agora = datetime.now()
    chave_mes = f"{agora.year}-{agora.month:02d}"

    if "calendario" not in dados:
        dados["calendario"] = {}

    if chave_mes not in dados["calendario"]:
        dados["calendario"][chave_mes] = {}

    dados["calendario"][chave_mes][str(agora.day)] = status
    return salvar_dados(dados)


def registrar_atividade_diaria(dados):
    """Registra atividades realizadas no dia atual"""
    limpar_tela()
    print(f"\n{Cor.CIANO_B}{'━' * 80}{Cor.RESET}")
    print(
        f"{Cor.BOLD}{Cor.CIANO_B}{'🔥 REGISTRAR ATIVIDADES DE HOJE'.center(80)}{Cor.RESET}"
    )
    print(f"{Cor.CIANO_B}{'━' * 80}{Cor.RESET}\n")

    hoje = datetime.now()
    chave_hoje = hoje.strftime("%Y-%m-%d")

    # Obter ou criar registro de hoje
    if chave_hoje not in dados["atividades_diarias"]:
        dados["atividades_diarias"][chave_hoje] = {"atividades": {}, "nivel": 0}

    atividades_hoje = dados["atividades_diarias"][chave_hoje]

    # Lista de atividades comuns
    atividades_sugeridas = [
        "Exercício físico",
        "Meditação",
        "Leitura",
        "Estudo",
        "Programação",
        "Escrita",
        "Arte/Criatividade",
        "Trabalho/Projetos",
    ]

    print(f"{Cor.BOLD}ATIVIDADES SUGERIDAS:{Cor.RESET}")
    print(f"{Cor.DIM}{'─' * 80}{Cor.RESET}\n")

    for i, atividade in enumerate(atividades_sugeridas, 1):
        count = atividades_hoje["atividades"].get(atividade, 0)
        status_visual = (
            f"{Cor.VERDE_B}✓ {count}x{Cor.RESET}"
            if count > 0
            else f"{Cor.DIM}○{Cor.RESET}"
        )
        print(f"  {i}. {status_visual} {atividade}")

    print(f"\n  {Cor.BOLD}0.{Cor.RESET} Atividade personalizada")
    print(f"\n{Cor.DIM}{'─' * 80}{Cor.RESET}")
    print(
        f"{Cor.BOLD}Digite o número da atividade realizada (ou Enter para voltar):{Cor.RESET}"
    )

    escolha = input(f"\n{Cor.CIANO}❯{Cor.RESET} ").strip()

    if not escolha:
        return

    try:
        idx = int(escolha)

        if idx == 0:
            # Atividade personalizada
            custom = input(f"\n{Cor.CIANO}Nome da atividade:{Cor.RESET} ").strip()
            if custom:
                atividade_escolhida = custom
            else:
                return
        elif 1 <= idx <= len(atividades_sugeridas):
            atividade_escolhida = atividades_sugeridas[idx - 1]
        else:
            mostrar_feedback("Número inválido!", "erro")
            return

        # Incrementar contador
        if atividade_escolhida not in atividades_hoje["atividades"]:
            atividades_hoje["atividades"][atividade_escolhida] = 0

        atividades_hoje["atividades"][atividade_escolhida] += 1

        # Calcular nível baseado no total de atividades
        total_atividades = sum(atividades_hoje["atividades"].values())

        if total_atividades == 0:
            nivel = 0
        elif total_atividades <= 2:
            nivel = 1
        elif total_atividades <= 4:
            nivel = 2
        elif total_atividades <= 6:
            nivel = 3
        else:
            nivel = 4

        atividades_hoje["nivel"] = nivel

        if salvar_dados(dados):
            mostrar_feedback(
                f"✓ {atividade_escolhida} registrada! Total hoje: {total_atividades}",
                "sucesso",
            )

    except ValueError:
        mostrar_feedback("Entrada inválida!", "erro")


# ============== INTERFACE ==============
def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def obter_emoji_prioridade(prioridade):
    """Retorna emoji e cor baseado na prioridade"""
    config = {
        1: ("🔴", Cor.VERMELHO_B),
        2: ("🟡", Cor.AMARELO_B),
        3: ("🟢", Cor.VERDE_B),
    }
    return config.get(prioridade, ("⚪", Cor.RESET))


def calcular_estatisticas(tarefas, caderno):
    """Calcula estatísticas das tarefas"""
    tarefas_caderno = [
        t for t in tarefas if caderno in t.get("cadernos", [t["caderno"]])
    ]
    total = len(tarefas_caderno)
    concluidas = sum(1 for t in tarefas_caderno if t["status"] == "X")
    progresso = int((concluidas / total * 100)) if total > 0 else 0
    return total, concluidas, progresso


def criar_barra_progresso(progresso, largura=20):
    """Cria uma barra de progresso colorida"""
    num_blocos = int(progresso / 100 * largura)

    if progresso >= 80:
        cor = Cor.VERDE_B
    elif progresso >= 50:
        cor = Cor.AMARELO_B
    elif progresso > 0:
        cor = Cor.VERMELHO_B
    else:
        cor = Cor.DIM

    barra = f"{cor}{'█' * num_blocos}{Cor.RESET}{Cor.DIM}{'░' * (largura - num_blocos)}{Cor.RESET}"
    return barra


def mostrar_selecao_caderno(dados):
    """Mostra tela de seleção de caderno com visual de cards"""
    limpar_tela()

    data_hoje = datetime.now().strftime("%d/%m/%Y")
    hora_atual = datetime.now().strftime("%H:%M")
    dia_semana = datetime.now().strftime("%A")

    # Tradução do dia da semana
    dias_pt = {
        "Monday": "Segunda-feira",
        "Tuesday": "Terça-feira",
        "Wednesday": "Quarta-feira",
        "Thursday": "Quinta-feira",
        "Friday": "Sexta-feira",
        "Saturday": "Sábado",
        "Sunday": "Domingo",
    }
    dia_semana = dias_pt.get(dia_semana, dia_semana)

    LARGURA = 100

    # ============== CABEÇALHO ==============

    print(
        f"{Cor.DIM}{f'{dia_semana} • {data_hoje} • {hora_atual}'.center(LARGURA)}{Cor.RESET}"
    )
    print(f"{Cor.CIANO_B}{'━' * LARGURA}{Cor.RESET}\n")

    print(f"{Cor.BOLD}📚 ESCOLHA SEU CADERNO{Cor.RESET}")
    print(f"{Cor.DIM}{'─' * LARGURA}{Cor.RESET}\n")

    # ============== CARDS DOS CADERNOS ==============
    cadernos = dados["cadernos"]
    tarefas = dados["tarefas"]

    # Emojis para cada tipo de caderno
    emojis_caderno = {
        "Hoje": "📋",
        "Faculdade": "🎓",
        "Trabalho": "💼",
        "Projetos": "🚀",
        "Pessoal": "✨",
        "Saúde": "💪",
        "Estudos": "📚",
        "Casa": "🏠",
    }

    # Cores para cada caderno
    cores_caderno = [
        Cor.CIANO_B,
        Cor.MAGENTA_B,
        Cor.VERDE_B,
        Cor.AMARELO_B,
        Cor.AZUL_B,
        Cor.VERMELHO_B,
    ]

    # Mostrar cards em grid 3x2 (ou adaptável)
    cards_por_linha = 3

    for i in range(0, len(cadernos), cards_por_linha):
        linha_cadernos = cadernos[i : i + cards_por_linha]

        # Linha superior dos cards
        for j, caderno in enumerate(linha_cadernos):
            cor_card = cores_caderno[(i + j) % len(cores_caderno)]
            print(f"  {cor_card}┌{'─' * 28}┐{Cor.RESET}", end="  ")
        print()

        # Linha do número e emoji
        for j, caderno in enumerate(linha_cadernos):
            cor_card = cores_caderno[(i + j) % len(cores_caderno)]
            emoji = emojis_caderno.get(caderno, "📓")
            numero = i + j + 1
            print(
                f"  {cor_card}│{Cor.RESET} {Cor.BOLD}{numero}.{Cor.RESET} {emoji}  {Cor.BOLD}{caderno:<21}{Cor.RESET} {cor_card}│{Cor.RESET}",
                end="  ",
            )
        print()

        # Linha separadora
        for j, caderno in enumerate(linha_cadernos):
            cor_card = cores_caderno[(i + j) % len(cores_caderno)]
            print(f"  {cor_card}├{'─' * 28}┤{Cor.RESET}", end="  ")
        print()

        # Linha de estatísticas
        for j, caderno in enumerate(linha_cadernos):
            cor_card = cores_caderno[(i + j) % len(cores_caderno)]
            total, concl, prog = calcular_estatisticas(tarefas, caderno)
            print(
                f"  {cor_card}│{Cor.RESET}  {Cor.DIM}Tarefas:{Cor.RESET} {total:<15}{cor_card}│{Cor.RESET}",
                end="  ",
            )
        print()

        for j, caderno in enumerate(linha_cadernos):
            cor_card = cores_caderno[(i + j) % len(cores_caderno)]
            total, concl, prog = calcular_estatisticas(tarefas, caderno)
            print(
                f"  {cor_card}│{Cor.RESET}  {Cor.VERDE_B}✓{Cor.RESET} Concluídas: {concl:<10}{cor_card}│{Cor.RESET}",
                end="  ",
            )
        print()

        # Barra de progresso
        for j, caderno in enumerate(linha_cadernos):
            cor_card = cores_caderno[(i + j) % len(cores_caderno)]
            total, concl, prog = calcular_estatisticas(tarefas, caderno)
            barra_mini = criar_barra_progresso(prog, 18)
            print(
                f"  {cor_card}│{Cor.RESET}  {barra_mini} {prog:>3}% {cor_card}│{Cor.RESET}",
                end="  ",
            )
        print()

        # Linha inferior dos cards
        for j, caderno in enumerate(linha_cadernos):
            cor_card = cores_caderno[(i + j) % len(cores_caderno)]
            print(f"  {cor_card}└{'─' * 28}┘{Cor.RESET}", end="  ")
        print("\n")

    # ============== OPÇÕES ==============
    print(f"{Cor.DIM}{'─' * LARGURA}{Cor.RESET}")
    print(f"{Cor.BOLD}COMANDOS:{Cor.RESET}")
    print(f"  {Cor.BOLD}1-{len(cadernos)}{Cor.RESET} Selecionar caderno")
    print(
        f"  {Cor.BOLD}[N]{Cor.RESET} Novo caderno  {Cor.BOLD}[R]{Cor.RESET} Remover caderno  {Cor.BOLD}[Q]{Cor.RESET} Sair"
    )
    print(f"{Cor.DIM}{'─' * LARGURA}{Cor.RESET}\n")

    return True


def mostrar_interface(dados):
    limpar_tela()
    LARGURA = 100

    cadernos = dados["cadernos"]
    caderno_atual = dados["caderno_ativo"]
    tarefas = dados["tarefas"]
    metas = dados.get("metas", {"semanais": [], "mensais": [], "anuais": []})

    data_hoje = datetime.now().strftime("%d/%m/%Y")
    hora_atual = datetime.now().strftime("%H:%M")
    dia_semana = datetime.now().strftime("%A")

    # Tradução do dia da semana
    dias_pt = {
        "Monday": "Segunda-feira",
        "Tuesday": "Terça-feira",
        "Wednesday": "Quarta-feira",
        "Thursday": "Quinta-feira",
        "Friday": "Sexta-feira",
        "Saturday": "Sábado",
        "Sunday": "Domingo",
    }
    dia_semana = dias_pt.get(dia_semana, dia_semana)

    # ============== CABEÇALHO PRINCIPAL ==============
    print(
        f"{Cor.DIM}{f'{dia_semana} • {data_hoje} • {hora_atual}'.center(LARGURA)}{Cor.RESET}"
    )
    print(f"{Cor.CIANO_B}{'━' * LARGURA}{Cor.RESET}\n")

    # ============== LAYOUT DUAS COLUNAS: TAREFAS E METAS ==============
    total_tarefas, concluidas, progresso = calcular_estatisticas(tarefas, caderno_atual)

    # Largura das colunas
    LARGURA_COLUNA_ESQ = 55  # Tarefas
    LARGURA_COLUNA_DIR = 43  # Metas

    # Filtrar e ordenar tarefas
    tarefas_filtradas = [
        t for t in tarefas if caderno_atual in t.get("cadernos", [t["caderno"]])
    ]
    tarefas_filtradas.sort(key=lambda x: (x["status"] == "X", -x.get("prioridade", 2)))

    # Agrupar por status
    pendentes = [t for t in tarefas_filtradas if t["status"] != "X"]
    concluidas_lista = [t for t in tarefas_filtradas if t["status"] == "X"]

    # Preparar metas semanais
    metas_semanais = metas.get("semanais", [])

    # ============== CABEÇALHOS DAS COLUNAS ==============
    print(
        f"{Cor.BOLD}✓ TAREFAS • {caderno_atual.upper():<40}{Cor.RESET}  {Cor.BOLD}🎯 METAS SEMANAIS{Cor.RESET}"
    )
    print(f"{Cor.DIM}{'─' * LARGURA_COLUNA_ESQ}  {'─' * LARGURA_COLUNA_DIR}{Cor.RESET}")

    # Barra de progresso tarefas
    barra_geral = criar_barra_progresso(progresso, 35)
    linha_prog_tarefas = f"  {barra_geral} {Cor.BOLD}{progresso}%{Cor.RESET} {Cor.DIM}({concluidas}/{total_tarefas}){Cor.RESET}"

    # Calcular média das metas
    if metas_semanais:
        media_prog = sum(m.get("progresso", 0) for m in metas_semanais) / len(
            metas_semanais
        )
        barra_metas = criar_barra_progresso(int(media_prog), 25)
        linha_prog_metas = f"{barra_metas} {Cor.BOLD}{int(media_prog)}%{Cor.RESET}"
    else:
        linha_prog_metas = f"{Cor.DIM}Nenhuma meta definida{Cor.RESET}"

    # Alinhar as barras de progresso
    espacos_esq = LARGURA_COLUNA_ESQ - len_visual(linha_prog_tarefas)
    print(f"{linha_prog_tarefas}{' ' * espacos_esq}  {linha_prog_metas}")
    print()

    # ============== CONSTRUIR LINHAS DA TABELA ==============
    linhas_tarefas = []
    linhas_metas = []

    # Preparar linhas de tarefas
    if not tarefas_filtradas:
        linhas_tarefas.append(f"{Cor.DIM}Nenhuma tarefa ainda{Cor.RESET}")
        linhas_tarefas.append(f"{Cor.DIM}Use [+] para adicionar!{Cor.RESET}")
    else:
        # Pendentes
        if pendentes:
            linhas_tarefas.append(f"{Cor.AMARELO_B}⚡ PENDENTES{Cor.RESET}")
            for t in pendentes[:8]:  # Limitar para não ficar muito longo
                emoji, cor = obter_emoji_prioridade(t.get("prioridade", 2))
                id_str = f"{cor}#{t['id']:02d}{Cor.RESET}"

                # Truncar texto se muito longo
                texto_tarefa = t["texto"]
                if len_visual(texto_tarefa) > 35:
                    texto_tarefa = texto_tarefa[:32] + "..."

                # Indicador de múltiplos cadernos
                multi_caderno = ""
                cadernos_extras = [
                    c for c in t.get("cadernos", []) if c != caderno_atual
                ]
                if cadernos_extras:
                    if len(cadernos_extras) == 1:
                        multi_caderno = f" {Cor.DIM}+{Cor.RESET}"
                    else:
                        multi_caderno = f" {Cor.DIM}+{len(cadernos_extras)}{Cor.RESET}"

                linhas_tarefas.append(
                    f"  {id_str} {emoji} {texto_tarefa}{multi_caderno}"
                )

            if len(pendentes) > 8:
                linhas_tarefas.append(
                    f"  {Cor.DIM}... e mais {len(pendentes) - 8} tarefas{Cor.RESET}"
                )
            linhas_tarefas.append("")

        # Concluídas (compacto)
        if concluidas_lista:
            linhas_tarefas.append(
                f"{Cor.VERDE_B}✓ CONCLUÍDAS ({len(concluidas_lista)}){Cor.RESET}"
            )
            for t in concluidas_lista[:3]:
                emoji, cor = obter_emoji_prioridade(t.get("prioridade", 2))
                id_str = f"{cor}#{t['id']:02d}{Cor.RESET}"

                texto_tarefa = t["texto"]
                if len_visual(texto_tarefa) > 35:
                    texto_tarefa = texto_tarefa[:32] + "..."

                linhas_tarefas.append(
                    f"  {id_str} {Cor.DIM}✓ {texto_tarefa}{Cor.RESET}"
                )

            if len(concluidas_lista) > 3:
                linhas_tarefas.append(
                    f"  {Cor.DIM}... e mais {len(concluidas_lista) - 3}{Cor.RESET}"
                )

    # Preparar linhas de metas
    if not metas_semanais:
        linhas_metas.append(f"{Cor.DIM}Use [M] para criar metas!{Cor.RESET}")
    else:
        for idx, meta in enumerate(metas_semanais[:6], 1):
            prog = meta.get("progresso", 0)
            texto = meta.get("texto", "")

            # Truncar texto se muito longo
            if len_visual(texto) > 35:
                texto = texto[:32] + "..."

            # Destaque para semana atual
            if meta.get("tipo") == "semana_atual":
                texto = f"{Cor.CIANO_B}⭐ {texto}{Cor.RESET}"

            barra = criar_barra_progresso(prog, 25)

            linhas_metas.append(f"{Cor.BOLD}{idx}.{Cor.RESET} {texto}")
            linhas_metas.append(f"   {barra} {Cor.BOLD}{prog}%{Cor.RESET}")
            linhas_metas.append("")

    # ============== RENDERIZAR DUAS COLUNAS ==============
    max_linhas = max(len(linhas_tarefas), len(linhas_metas))

    for i in range(max_linhas):
        # Coluna esquerda (tarefas)
        if i < len(linhas_tarefas):
            linha_esq = linhas_tarefas[i]
        else:
            linha_esq = ""

        # Coluna direita (metas)
        if i < len(linhas_metas):
            linha_dir = linhas_metas[i]
        else:
            linha_dir = ""

        # Calcular espaçamento
        espacos = LARGURA_COLUNA_ESQ - len_visual(linha_esq)
        print(f"{linha_esq}{' ' * espacos}  {linha_dir}")

    print()
    print(
        f"{Cor.DIM}[+] Adicionar  [X] Concluir  [E] Editar  [D] Deletar  [P] Prioridade  [M] Metas{Cor.RESET}"
    )
    print(f"{Cor.AZUL}{'─' * LARGURA}{Cor.RESET}\n")

    # ============== REVIEW HEATMAP ==============
    print(f"{Cor.BOLD}🔥 REVIEW HEATMAP • SEMANA ATUAL{Cor.RESET}")
    print(f"{Cor.DIM}{'─' * LARGURA}{Cor.RESET}")

    # Obter atividades diárias
    atividades_diarias = dados.get("atividades_diarias", {})

    # Calcular dias da semana atual
    hoje = datetime.now()
    dia_semana_num = hoje.weekday()  # 0=Segunda, 6=Domingo

    # Calcular primeira segunda-feira da semana
    inicio_semana = hoje - timedelta(days=dia_semana_num)

    # Dias da semana em português (abreviado)
    dias_semana_curtos = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]

    # Criar linha de dias da semana
    linha_dias = "  "
    for i, dia_nome in enumerate(dias_semana_curtos):
        linha_dias += f"{Cor.BOLD}{dia_nome:^5}{Cor.RESET} "
    print(linha_dias)

    # Criar linha de heatmap
    linha_heat = "  "
    for i in range(7):
        dia_atual = inicio_semana + timedelta(days=i)
        chave_dia = dia_atual.strftime("%Y-%m-%d")

        # Verificar se é hoje
        eh_hoje = dia_atual.date() == hoje.date()

        # Obter status do dia
        status = atividades_diarias.get(chave_dia, {})
        nivel = status.get("nivel", 0)  # 0-4

        # Escolher cor baseado no nível
        if nivel == 0:
            cor_quadrado = Cor.DIM
            char = "░"
        elif nivel == 1:
            cor_quadrado = Cor.VERDE
            char = "▓"
        elif nivel == 2:
            cor_quadrado = Cor.VERDE_B
            char = "▓"
        elif nivel == 3:
            cor_quadrado = Cor.AMARELO_B
            char = "▓"
        else:  # nivel 4
            cor_quadrado = Cor.CIANO_B
            char = "█"

        # Destacar dia de hoje
        if eh_hoje:
            linha_heat += f"{Cor.BG_AZUL}{Cor.BRANCO} {char * 3} {Cor.RESET} "
        else:
            linha_heat += f"{cor_quadrado}{char * 3}{char * 2}{Cor.RESET} "

    print(linha_heat)

    # Legenda compacta
    print(
        f"\n  {Cor.DIM}░░{Cor.RESET} Nada  {Cor.VERDE}▓▓{Cor.RESET} Pouco  {Cor.VERDE_B}▓▓{Cor.RESET} Médio  {Cor.AMARELO_B}▓▓{Cor.RESET} Muito  {Cor.CIANO_B}██{Cor.RESET} Excelente"
    )

    # Mostrar contador de atividades de hoje
    chave_hoje = hoje.strftime("%Y-%m-%d")
    atividades_hoje = atividades_diarias.get(chave_hoje, {})
    total_hoje = sum(atividades_hoje.get("atividades", {}).values())

    if total_hoje > 0:
        print(
            f"\n  {Cor.CIANO_B}📊 Hoje: {total_hoje} atividade(s) registrada(s){Cor.RESET}"
        )
    else:
        print(f"\n  {Cor.DIM}💭 Nenhuma atividade registrada hoje ainda{Cor.RESET}")

    print()
    print(f"{Cor.DIM}[H] Heatmap  [S] Estatísticas  [A] Notas{Cor.RESET}")
    print(f"{Cor.AZUL}{'─' * LARGURA}{Cor.RESET}\n")

    # ============== MENU DE COMANDOS ==============
    print(f"{Cor.CIANO_B}{'━' * LARGURA}{Cor.RESET}")
    print(
        f"{Cor.BOLD}COMANDOS{Cor.RESET} -> {Cor.BOLD}C{Cor.RESET} Menu cadernos {Cor.BOLD}Q{Cor.RESET} Sair"
    )

    print(f"{Cor.CIANO_B}{'━' * LARGURA}{Cor.RESET}\n")


def gerenciar_metas(dados):
    """Interface para gerenciar metas semanais, mensais e anuais"""
    if "metas" not in dados:
        dados["metas"] = {"semanais": [], "mensais": [], "anuais": []}

    tipo_atual = "semanais"
    mes_selecionado = datetime.now().month  # Mês atual (1-12)

    while True:
        limpar_tela()

        # Header
        print(f"\n{Cor.MAGENTA_B}{'━' * 100}{Cor.RESET}")
        print(
            f"{Cor.BOLD}{Cor.MAGENTA_B}{'🎯 GERENCIADOR DE METAS'.center(100)}{Cor.RESET}"
        )
        print(f"{Cor.MAGENTA_B}{'━' * 100}{Cor.RESET}\n")

        # Tabs
        tabs = []
        for tipo in ["semanais", "mensais", "anuais", "calendario"]:
            if tipo == tipo_atual:
                tab_nome = "CALENDÁRIO" if tipo == "calendario" else tipo.upper()
                tabs.append(f"{Cor.BG_AZUL}{Cor.BRANCO} {tab_nome} {Cor.RESET}")
            else:
                tab_nome = "Calendário" if tipo == "calendario" else tipo.capitalize()
                tabs.append(f"{Cor.DIM}[{tab_nome}]{Cor.RESET}")

        print("  " + "   ".join(tabs))
        print(f"\n{Cor.DIM}{'─' * 100}{Cor.RESET}\n")

        # Mostrar calendário ou metas
        if tipo_atual == "calendario":
            # Mostrar calendário do mês atual
            agora = datetime.now()
            chave_mes = f"{agora.year}-{agora.month:02d}"

            # Obter dias marcados
            dias_marcados = dados.get("calendario", {}).get(chave_mes, {})
            dias_marcados_int = {int(k): v for k, v in dias_marcados.items()}

            # Criar e mostrar calendário
            cal_visual = criar_calendario_mensal(
                agora.year, agora.month, dias_marcados_int
            )

            # Centralizar calendário
            for linha in cal_visual.split("\n"):
                print(f"  {linha}")

            print(f"\n{Cor.DIM}{'─' * 100}{Cor.RESET}")
            print(f"\n{Cor.BOLD}MARCAR DIA DE HOJE:{Cor.RESET}")
            print(
                f"  {Cor.VERDE_B}[C]{Cor.RESET} Completo  {Cor.AMARELO_B}[P]{Cor.RESET} Parcial  {Cor.VERMELHO_B}[F]{Cor.RESET} Falha  {Cor.DIM}[L]{Cor.RESET} Limpar marca"
            )

        elif tipo_atual == "mensais":
            # Mostrar seletor de mês
            meses_pt = [
                "Janeiro",
                "Fevereiro",
                "Março",
                "Abril",
                "Maio",
                "Junho",
                "Julho",
                "Agosto",
                "Setembro",
                "Outubro",
                "Novembro",
                "Dezembro",
            ]

            print(
                f"{Cor.BOLD}{Cor.MAGENTA_B}📅 {meses_pt[mes_selecionado - 1].upper()}{Cor.RESET}"
            )
            print(f"{Cor.DIM}{'─' * 100}{Cor.RESET}\n")

            # Navegação entre meses
            navegacao = []
            for i, mes_nome in enumerate(meses_pt, 1):
                if i == mes_selecionado:
                    navegacao.append(
                        f"{Cor.BG_AZUL}{Cor.BRANCO} {mes_nome[:3]} {Cor.RESET}"
                    )
                elif i == datetime.now().month:
                    navegacao.append(f"{Cor.CIANO_B}{mes_nome[:3]}{Cor.RESET}")
                else:
                    navegacao.append(f"{Cor.DIM}{mes_nome[:3]}{Cor.RESET}")

            # Exibir navegação em linhas
            print("  " + "  ".join(navegacao[:6]))
            print("  " + "  ".join(navegacao[6:]))
            print(
                f"\n{Cor.DIM}Use ← e → ou números 5-16 para navegar entre os meses{Cor.RESET}"
            )
            print(f"{Cor.DIM}{'─' * 100}{Cor.RESET}\n")

            # Filtrar metas do mês selecionado
            mes_nome_completo = meses_pt[mes_selecionado - 1]
            metas_do_mes = [
                (i, meta)
                for i, meta in enumerate(dados["metas"].get("mensais", []))
                if mes_nome_completo in meta.get("texto", "")
            ]

            if not metas_do_mes:
                print(
                    f"{Cor.DIM}  Nenhuma meta cadastrada para {mes_nome_completo}.{Cor.RESET}\n"
                )
            else:
                for display_idx, (real_idx, meta) in enumerate(metas_do_mes, 1):
                    texto = meta.get("texto", "")
                    prog = meta.get("progresso", 0)
                    barra = criar_barra_progresso(prog, 40)

                    # Destacar mês atual
                    destaque = ""
                    if mes_selecionado == datetime.now().month:
                        destaque = f" {Cor.CIANO_B}⭐ MÊS ATUAL{Cor.RESET}"

                    print(f"  {Cor.BOLD}{display_idx}.{Cor.RESET} {texto}{destaque}")
                    print(f"     {barra}  {Cor.BOLD}{prog}%{Cor.RESET}\n")

        else:
            # Mostrar metas do tipo atual (semanais ou anuais)
            metas_tipo = dados["metas"].get(tipo_atual, [])

            if not metas_tipo:
                print(
                    f"{Cor.DIM}  Nenhuma meta {tipo_atual[:-2]} cadastrada.{Cor.RESET}\n"
                )
            else:
                for idx, meta in enumerate(metas_tipo, 1):
                    texto = meta.get("texto", "")
                    prog = meta.get("progresso", 0)
                    barra = criar_barra_progresso(prog, 40)

                    # Destacar semana atual
                    destaque = ""
                    if meta.get("tipo") == "semana_atual":
                        destaque = f" {Cor.CIANO_B}⭐ SEMANA ATUAL{Cor.RESET}"

                    print(f"  {Cor.BOLD}{idx}.{Cor.RESET} {texto}{destaque}")
                    print(f"     {barra}  {Cor.BOLD}{prog}%{Cor.RESET}\n")

        # Menu
        print(f"{Cor.DIM}{'─' * 100}{Cor.RESET}")
        print(f"{Cor.BOLD}COMANDOS:{Cor.RESET}")
        print(
            f"  {Cor.BOLD}[1]{Cor.RESET} Semanais  {Cor.BOLD}[2]{Cor.RESET} Mensais  {Cor.BOLD}[3]{Cor.RESET} Anuais  {Cor.BOLD}[4]{Cor.RESET} Calendário"
        )

        if tipo_atual != "calendario":
            print(
                f"  {Cor.BOLD}[+]{Cor.RESET} Nova meta  {Cor.BOLD}[E]{Cor.RESET} Editar  {Cor.BOLD}[U]{Cor.RESET} Atualizar progresso  {Cor.BOLD}[D]{Cor.RESET} Deletar"
            )

        print(f"  {Cor.BOLD}[V]{Cor.RESET} Voltar")
        print(f"{Cor.DIM}{'─' * 100}{Cor.RESET}\n")

        cmd = input(f"{Cor.CIANO}❯{Cor.RESET} ").lower().strip()

        # Navegação entre meses (para metas mensais)
        if tipo_atual == "mensais":
            # Seta esquerda ou < para mês anterior
            if cmd in ["<", "←"]:
                mes_selecionado = mes_selecionado - 1 if mes_selecionado > 1 else 12
                continue
            # Seta direita ou > para próximo mês
            elif cmd in [">", "→"]:
                mes_selecionado = mes_selecionado + 1 if mes_selecionado < 12 else 1
                continue
            # Números 5-16 para selecionar mês diretamente
            elif cmd.isdigit() and 5 <= int(cmd) <= 16:
                mes_selecionado = int(cmd) - 4
                continue

        # Trocar tipo de meta
        if cmd == "1":
            tipo_atual = "semanais"
        elif cmd == "2":
            tipo_atual = "mensais"
        elif cmd == "3":
            tipo_atual = "anuais"
        elif cmd == "4":
            tipo_atual = "calendario"

        # Marcar dia no calendário
        elif cmd == "c" and tipo_atual == "calendario":
            if marcar_dia_calendario(dados, "completo"):
                mostrar_feedback("Dia marcado como completo! ✓", "sucesso")
        elif cmd == "p" and tipo_atual == "calendario":
            if marcar_dia_calendario(dados, "parcial"):
                mostrar_feedback("Dia marcado como parcial!", "aviso")
        elif cmd == "f" and tipo_atual == "calendario":
            if marcar_dia_calendario(dados, "falha"):
                mostrar_feedback("Dia marcado como pendente.", "erro")
        elif cmd == "l" and tipo_atual == "calendario":
            agora = datetime.now()
            chave_mes = f"{agora.year}-{agora.month:02d}"
            if chave_mes in dados.get("calendario", {}):
                if str(agora.day) in dados["calendario"][chave_mes]:
                    del dados["calendario"][chave_mes][str(agora.day)]
                    if salvar_dados(dados):
                        mostrar_feedback("Marca removida do dia!", "info")

        # Adicionar nova meta
        elif cmd == "+" and tipo_atual != "calendario":
            print(
                f"\n{Cor.VERDE_B}➕ NOVA META {tipo_atual.upper()[:-2].upper()}{Cor.RESET}"
            )
            print(f"{Cor.DIM}{'─' * 60}{Cor.RESET}")
            texto = input(f"Descrição: ").strip()
            if texto:
                try:
                    prog = input(f"Progresso inicial (0-100) [0]: ").strip()
                    prog = int(prog) if prog else 0
                    prog = min(max(prog, 0), 100)
                except:
                    prog = 0

                dados["metas"][tipo_atual].append({"texto": texto, "progresso": prog})

                if salvar_dados(dados):
                    mostrar_feedback("Meta adicionada com sucesso!", "sucesso")

        # Editar meta
        elif cmd == "e" and tipo_atual != "calendario":
            if tipo_atual == "mensais":
                # Para metas mensais, usar a lista filtrada
                meses_pt = [
                    "Janeiro",
                    "Fevereiro",
                    "Março",
                    "Abril",
                    "Maio",
                    "Junho",
                    "Julho",
                    "Agosto",
                    "Setembro",
                    "Outubro",
                    "Novembro",
                    "Dezembro",
                ]
                mes_nome_completo = meses_pt[mes_selecionado - 1]
                metas_do_mes = [
                    (i, meta)
                    for i, meta in enumerate(dados["metas"]["mensais"])
                    if mes_nome_completo in meta.get("texto", "")
                ]

                if metas_do_mes:
                    try:
                        idx_display = (
                            int(input(f"\n{Cor.AZUL}Número da meta:{Cor.RESET} ")) - 1
                        )
                        if 0 <= idx_display < len(metas_do_mes):
                            real_idx, meta = metas_do_mes[idx_display]
                            print(f"{Cor.DIM}Texto atual: {meta['texto']}{Cor.RESET}")
                            novo_texto = input(
                                f"Novo texto (Enter para manter): "
                            ).strip()
                            if novo_texto:
                                dados["metas"]["mensais"][real_idx]["texto"] = (
                                    novo_texto
                                )
                                if salvar_dados(dados):
                                    mostrar_feedback("Meta editada!", "sucesso")
                        else:
                            mostrar_feedback("Número inválido!", "erro")
                    except:
                        mostrar_feedback("Entrada inválida!", "erro")
                else:
                    mostrar_feedback("Nenhuma meta para editar!", "aviso")
            else:
                # Para semanais e anuais, usar lógica normal
                metas_tipo = dados["metas"].get(tipo_atual, [])
                if metas_tipo:
                    try:
                        idx = int(input(f"\n{Cor.AZUL}Número da meta:{Cor.RESET} ")) - 1
                        if 0 <= idx < len(metas_tipo):
                            print(
                                f"{Cor.DIM}Texto atual: {metas_tipo[idx]['texto']}{Cor.RESET}"
                            )
                            novo_texto = input(
                                f"Novo texto (Enter para manter): "
                            ).strip()
                            if novo_texto:
                                metas_tipo[idx]["texto"] = novo_texto
                                if salvar_dados(dados):
                                    mostrar_feedback("Meta editada!", "sucesso")
                        else:
                            mostrar_feedback("Número inválido!", "erro")
                    except:
                        mostrar_feedback("Entrada inválida!", "erro")
                else:
                    mostrar_feedback("Nenhuma meta para editar!", "aviso")

        # Atualizar progresso
        elif cmd == "u" and tipo_atual != "calendario":
            if tipo_atual == "mensais":
                # Para metas mensais, usar a lista filtrada
                meses_pt = [
                    "Janeiro",
                    "Fevereiro",
                    "Março",
                    "Abril",
                    "Maio",
                    "Junho",
                    "Julho",
                    "Agosto",
                    "Setembro",
                    "Outubro",
                    "Novembro",
                    "Dezembro",
                ]
                mes_nome_completo = meses_pt[mes_selecionado - 1]
                metas_do_mes = [
                    (i, meta)
                    for i, meta in enumerate(dados["metas"]["mensais"])
                    if mes_nome_completo in meta.get("texto", "")
                ]

                if metas_do_mes:
                    try:
                        idx_display = (
                            int(input(f"\n{Cor.AZUL}Número da meta:{Cor.RESET} ")) - 1
                        )
                        if 0 <= idx_display < len(metas_do_mes):
                            real_idx, meta = metas_do_mes[idx_display]
                            prog_atual = meta["progresso"]
                            print(f"{Cor.DIM}Progresso atual: {prog_atual}%{Cor.RESET}")
                            novo_prog = input(f"Novo progresso (0-100): ").strip()
                            if novo_prog:
                                novo_prog = int(novo_prog)
                                novo_prog = min(max(novo_prog, 0), 100)
                                dados["metas"]["mensais"][real_idx]["progresso"] = (
                                    novo_prog
                                )
                                if salvar_dados(dados):
                                    mostrar_feedback(
                                        f"Progresso atualizado para {novo_prog}%!",
                                        "sucesso",
                                    )
                        else:
                            mostrar_feedback("Número inválido!", "erro")
                    except:
                        mostrar_feedback("Entrada inválida!", "erro")
                else:
                    mostrar_feedback("Nenhuma meta para atualizar!", "aviso")
            else:
                # Para semanais e anuais, usar lógica normal
                metas_tipo = dados["metas"].get(tipo_atual, [])
                if metas_tipo:
                    try:
                        idx = int(input(f"\n{Cor.AZUL}Número da meta:{Cor.RESET} ")) - 1
                        if 0 <= idx < len(metas_tipo):
                            prog_atual = metas_tipo[idx]["progresso"]
                            print(f"{Cor.DIM}Progresso atual: {prog_atual}%{Cor.RESET}")
                            novo_prog = input(f"Novo progresso (0-100): ").strip()
                            if novo_prog:
                                novo_prog = int(novo_prog)
                                novo_prog = min(max(novo_prog, 0), 100)
                                metas_tipo[idx]["progresso"] = novo_prog
                                if salvar_dados(dados):
                                    mostrar_feedback(
                                        f"Progresso atualizado para {novo_prog}%!",
                                        "sucesso",
                                    )
                        else:
                            mostrar_feedback("Número inválido!", "erro")
                    except:
                        mostrar_feedback("Entrada inválida!", "erro")
                else:
                    mostrar_feedback("Nenhuma meta para atualizar!", "aviso")

        # Deletar meta
        elif cmd == "d" and tipo_atual != "calendario":
            if tipo_atual == "mensais":
                # Para metas mensais, usar a lista filtrada
                meses_pt = [
                    "Janeiro",
                    "Fevereiro",
                    "Março",
                    "Abril",
                    "Maio",
                    "Junho",
                    "Julho",
                    "Agosto",
                    "Setembro",
                    "Outubro",
                    "Novembro",
                    "Dezembro",
                ]
                mes_nome_completo = meses_pt[mes_selecionado - 1]
                metas_do_mes = [
                    (i, meta)
                    for i, meta in enumerate(dados["metas"]["mensais"])
                    if mes_nome_completo in meta.get("texto", "")
                ]

                if metas_do_mes:
                    try:
                        idx_display = (
                            int(
                                input(
                                    f"\n{Cor.VERMELHO}Número da meta para deletar:{Cor.RESET} "
                                )
                            )
                            - 1
                        )
                        if 0 <= idx_display < len(metas_do_mes):
                            real_idx, meta = metas_do_mes[idx_display]
                            confirma = input(
                                f"Confirma deletar '{meta['texto']}'? (s/n): "
                            ).lower()
                            if confirma == "s":
                                dados["metas"]["mensais"].pop(real_idx)
                                if salvar_dados(dados):
                                    mostrar_feedback("Meta deletada!", "sucesso")
                        else:
                            mostrar_feedback("Número inválido!", "erro")
                    except:
                        mostrar_feedback("Entrada inválida!", "erro")
                else:
                    mostrar_feedback("Nenhuma meta para deletar!", "aviso")
            else:
                # Para semanais e anuais, usar lógica normal
                metas_tipo = dados["metas"].get(tipo_atual, [])
                if metas_tipo:
                    try:
                        idx = (
                            int(
                                input(
                                    f"\n{Cor.VERMELHO}Número da meta para deletar:{Cor.RESET} "
                                )
                            )
                            - 1
                        )
                        if 0 <= idx < len(metas_tipo):
                            meta = metas_tipo[idx]
                            confirma = input(
                                f"Confirma deletar '{meta['texto']}'? (s/n): "
                            ).lower()
                            if confirma == "s":
                                metas_tipo.pop(idx)
                                if salvar_dados(dados):
                                    mostrar_feedback("Meta deletada!", "sucesso")
                        else:
                            mostrar_feedback("Número inválido!", "erro")
                    except:
                        mostrar_feedback("Entrada inválida!", "erro")
                else:
                    mostrar_feedback("Nenhuma meta para deletar!", "aviso")

        # Voltar
        elif cmd == "v":
            break


def mostrar_estatisticas_gerais(dados):
    """Mostra estatísticas gerais"""
    limpar_tela()
    LARGURA = 100

    print(f"\n{Cor.MAGENTA_B}{'━' * LARGURA}{Cor.RESET}")
    print(
        f"{Cor.BOLD}{Cor.MAGENTA_B}{'📊 ESTATÍSTICAS GERAIS'.center(LARGURA)}{Cor.RESET}"
    )
    print(f"{Cor.MAGENTA_B}{'━' * LARGURA}{Cor.RESET}\n")

    # Progresso por caderno
    print(f"{Cor.BOLD}PROGRESSO POR CADERNO{Cor.RESET}")
    print(f"{Cor.DIM}{'─' * LARGURA}{Cor.RESET}\n")

    for caderno in dados["cadernos"]:
        total, concluidas, progresso = calcular_estatisticas(dados["tarefas"], caderno)
        barra = criar_barra_progresso(progresso, 40)
        print(
            f"  {caderno:.<25} {barra}  {progresso:>3}%  {Cor.DIM}({concluidas}/{total}){Cor.RESET}"
        )

    print()

    # Resumo geral
    ids_unicos = set(t["id"] for t in dados["tarefas"])
    total_geral = len(ids_unicos)
    concluidas_geral = sum(
        1 for t in dados["tarefas"] if t["status"] == "X" and t["id"] in ids_unicos
    )
    pendentes_geral = total_geral - concluidas_geral

    print(f"{Cor.BOLD}RESUMO GERAL{Cor.RESET}")
    print(f"{Cor.DIM}{'─' * LARGURA}{Cor.RESET}\n")
    print(f"  Total de tarefas: {Cor.BOLD}{total_geral}{Cor.RESET}")
    print(f"  {Cor.VERDE_B}✓{Cor.RESET} Concluídas: {concluidas_geral}")
    print(f"  {Cor.AMARELO_B}○{Cor.RESET} Pendentes: {pendentes_geral}\n")

    # Metas
    print(f"{Cor.BOLD}RESUMO DE METAS{Cor.RESET}")
    print(f"{Cor.DIM}{'─' * LARGURA}{Cor.RESET}\n")

    metas = dados.get("metas", {"semanais": [], "mensais": [], "anuais": []})

    for tipo, nome in [
        ("semanais", "Semanais"),
        ("mensais", "Mensais"),
        ("anuais", "Anuais"),
    ]:
        metas_tipo = metas.get(tipo, [])
        if metas_tipo:
            media = sum(m.get("progresso", 0) for m in metas_tipo) / len(metas_tipo)
            barra = criar_barra_progresso(int(media), 30)
            print(f"  {nome:.<15} {barra}  {int(media):>3}%")

    if not any(metas.get(t, []) for t in ["semanais", "mensais", "anuais"]):
        print(f"  {Cor.DIM}Nenhuma meta cadastrada. Use [M] para criar!{Cor.RESET}")

    print(f"\n{Cor.DIM}{'─' * LARGURA}{Cor.RESET}")
    input(f"\n{Cor.DIM}Pressione ENTER para voltar...{Cor.RESET}")


def gerenciar_notas(dados):
    """Interface para notas"""
    caderno = dados["caderno_ativo"]

    while True:
        limpar_tela()
        LARGURA = 80

        print(f"\n{Cor.AMARELO_B}{'━' * LARGURA}{Cor.RESET}")
        print(
            f"{Cor.BOLD}{Cor.AMARELO_B}{'📝 NOTAS RÁPIDAS'.center(LARGURA)}{Cor.RESET}"
        )
        print(f"{Cor.AMARELO_B}{caderno.upper().center(LARGURA)}{Cor.RESET}")
        print(f"{Cor.AMARELO_B}{'━' * LARGURA}{Cor.RESET}\n")

        nota_atual = dados["notas"].get(caderno, "")

        if nota_atual:
            print(f"{Cor.DIM}┌{'─' * (LARGURA - 2)}┐{Cor.RESET}")
            for linha in nota_atual.split("\n"):
                print(
                    f"{Cor.DIM}│{Cor.RESET} {linha:<(LARGURA - 4)} {Cor.DIM}│{Cor.RESET}"
                )
            print(f"{Cor.DIM}└{'─' * (LARGURA - 2)}┘{Cor.RESET}\n")
        else:
            print(f"{Cor.DIM}  (Sem notas neste caderno){Cor.RESET}\n")

        print(f"{Cor.DIM}{'─' * LARGURA}{Cor.RESET}")
        print(
            f"{Cor.BOLD}[E]{Cor.RESET} Editar  {Cor.BOLD}[L]{Cor.RESET} Limpar  {Cor.BOLD}[V]{Cor.RESET} Voltar"
        )
        print(f"{Cor.DIM}{'─' * LARGURA}{Cor.RESET}\n")

        cmd = input(f"{Cor.CIANO}❯{Cor.RESET} ").lower().strip()

        if cmd == "e":
            print(
                f"\n{Cor.DIM}Digite suas notas (linha vazia para finalizar):{Cor.RESET}\n"
            )
            linhas = []
            while True:
                linha = input(f"{Cor.AMARELO}│{Cor.RESET} ")
                if linha == "":
                    break
                linhas.append(linha)
            dados["notas"][caderno] = "\n".join(linhas)
            if salvar_dados(dados):
                print(f"\n{Cor.VERDE_B}✓ Notas salvas com sucesso!{Cor.RESET}")
                input(f"{Cor.DIM}Pressione ENTER...{Cor.RESET}")
        elif cmd == "l":
            confirma = input(
                f"\n{Cor.AMARELO}Confirma limpar todas as notas? (s/n):{Cor.RESET} "
            ).lower()
            if confirma == "s":
                dados["notas"][caderno] = ""
                salvar_dados(dados)
                print(f"{Cor.VERDE_B}✓ Notas limpas!{Cor.RESET}")
                input(f"{Cor.DIM}Pressione ENTER...{Cor.RESET}")
        elif cmd == "v":
            break


def mostrar_feedback(mensagem, tipo="sucesso"):
    """Mostra feedback visual para ações"""
    cores = {
        "sucesso": Cor.VERDE_B,
        "erro": Cor.VERMELHO_B,
        "info": Cor.AZUL_B,
        "aviso": Cor.AMARELO_B,
    }
    icones = {"sucesso": "✓", "erro": "✗", "info": "ℹ", "aviso": "⚠"}

    cor = cores.get(tipo, Cor.RESET)
    icone = icones.get(tipo, "•")

    print(f"\n{cor}{icone} {mensagem}{Cor.RESET}")
    input(f"{Cor.DIM}Pressione ENTER...{Cor.RESET}")


# ============== LÓGICA PRINCIPAL ==============
def main():
    dados = carregar_dados()

    # Mostrar seleção de caderno primeiro
    while True:
        mostrar_selecao_caderno(dados)
        comando = input(f"{Cor.CIANO}❯{Cor.RESET} ").lower().strip()

        # Seleção de Caderno
        if comando.isdigit():
            idx = int(comando) - 1
            if 0 <= idx < len(dados["cadernos"]):
                dados["caderno_ativo"] = dados["cadernos"][idx]
                salvar_dados(dados)
                break  # Sai do loop e vai para a interface principal

        # Novo Caderno
        elif comando == "n":
            print(f"\n{Cor.AZUL_B}📚 NOVO CADERNO{Cor.RESET}")
            print(f"{Cor.DIM}{'─' * 50}{Cor.RESET}")
            novo_c = input(f"Nome: ").strip().title()
            if novo_c:
                if novo_c in dados["cadernos"]:
                    mostrar_feedback("Já existe um caderno com esse nome!", "aviso")
                else:
                    dados["cadernos"].append(novo_c)
                    if salvar_dados(dados):
                        mostrar_feedback(f"Caderno '{novo_c}' criado!", "sucesso")

        # Remover Caderno
        elif comando == "r":
            if len(dados["cadernos"]) <= 1:
                mostrar_feedback("Você precisa ter pelo menos um caderno!", "aviso")
            else:
                print(f"\n{Cor.VERMELHO}🗑️  REMOVER CADERNO{Cor.RESET}")
                print(f"{Cor.DIM}{'─' * 50}{Cor.RESET}")
                for i, c in enumerate(dados["cadernos"], 1):
                    n_tarefas = len(
                        [
                            t
                            for t in dados["tarefas"]
                            if c in t.get("cadernos", [t["caderno"]])
                        ]
                    )
                    print(f"  {i}. {c} ({n_tarefas} tarefas)")

                try:
                    idx = int(input(f"\nNúmero do caderno: ")) - 1
                    if 0 <= idx < len(dados["cadernos"]):
                        caderno_remover = dados["cadernos"][idx]

                        confirma = input(
                            f"\n{Cor.AMARELO}Remover '{caderno_remover}'? (As tarefas serão removidas apenas deste caderno) (s/n):{Cor.RESET} "
                        ).lower()
                        if confirma == "s":
                            dados["cadernos"].pop(idx)

                            # Remover o caderno da lista de cadernos de cada tarefa
                            for t in dados["tarefas"]:
                                if caderno_remover in t.get("cadernos", []):
                                    t["cadernos"].remove(caderno_remover)

                            # Remover tarefas que ficaram sem cadernos
                            dados["tarefas"] = [
                                t
                                for t in dados["tarefas"]
                                if len(t.get("cadernos", [])) > 0
                            ]

                            if dados["caderno_ativo"] == caderno_remover:
                                dados["caderno_ativo"] = dados["cadernos"][0]
                            if salvar_dados(dados):
                                mostrar_feedback("Caderno removido!", "sucesso")
                    else:
                        mostrar_feedback("Número inválido!", "erro")
                except:
                    mostrar_feedback("Entrada inválida!", "erro")

        # Sair
        elif comando == "q":
            limpar_tela()
            print(f"\n{Cor.CIANO_B}{'━' * 60}{Cor.RESET}")
            print(f"{Cor.BOLD}{Cor.CIANO_B}{'👋 Até logo!'.center(60)}{Cor.RESET}")
            print(
                f"{Cor.DIM}{'Seus dados foram salvos com sucesso.'.center(60)}{Cor.RESET}"
            )
            print(f"{Cor.CIANO_B}{'━' * 60}{Cor.RESET}\n")
            return

    # Loop principal da aplicação
    while True:
        mostrar_interface(dados)
        comando = input(f"{Cor.CIANO}❯{Cor.RESET} ").lower().strip()

        # Seleção de Caderno
        if comando.isdigit():
            idx = int(comando) - 1
            if 0 <= idx < len(dados["cadernos"]):
                dados["caderno_ativo"] = dados["cadernos"][idx]
                salvar_dados(dados)

        # Voltar ao menu de cadernos
        elif comando == "c":
            while True:
                mostrar_selecao_caderno(dados)
                sub_comando = input(f"{Cor.CIANO}❯{Cor.RESET} ").lower().strip()

                if sub_comando.isdigit():
                    idx = int(sub_comando) - 1
                    if 0 <= idx < len(dados["cadernos"]):
                        dados["caderno_ativo"] = dados["cadernos"][idx]
                        salvar_dados(dados)
                        break

                elif sub_comando == "n":
                    print(f"\n{Cor.AZUL_B}📚 NOVO CADERNO{Cor.RESET}")
                    print(f"{Cor.DIM}{'─' * 50}{Cor.RESET}")
                    novo_c = input(f"Nome: ").strip().title()
                    if novo_c:
                        if novo_c in dados["cadernos"]:
                            mostrar_feedback(
                                "Já existe um caderno com esse nome!", "aviso"
                            )
                        else:
                            dados["cadernos"].append(novo_c)
                            if salvar_dados(dados):
                                mostrar_feedback(
                                    f"Caderno '{novo_c}' criado!", "sucesso"
                                )

                elif sub_comando == "r":
                    if len(dados["cadernos"]) <= 1:
                        mostrar_feedback(
                            "Você precisa ter pelo menos um caderno!", "aviso"
                        )
                    else:
                        print(f"\n{Cor.VERMELHO}🗑️  REMOVER CADERNO{Cor.RESET}")
                        print(f"{Cor.DIM}{'─' * 50}{Cor.RESET}")
                        for i, c in enumerate(dados["cadernos"], 1):
                            n_tarefas = len(
                                [
                                    t
                                    for t in dados["tarefas"]
                                    if c in t.get("cadernos", [t["caderno"]])
                                ]
                            )
                            print(f"  {i}. {c} ({n_tarefas} tarefas)")

                        try:
                            idx = int(input(f"\nNúmero do caderno: ")) - 1
                            if 0 <= idx < len(dados["cadernos"]):
                                caderno_remover = dados["cadernos"][idx]

                                confirma = input(
                                    f"\n{Cor.AMARELO}Remover '{caderno_remover}'? (As tarefas serão removidas apenas deste caderno) (s/n):{Cor.RESET} "
                                ).lower()
                                if confirma == "s":
                                    dados["cadernos"].pop(idx)

                                    for t in dados["tarefas"]:
                                        if caderno_remover in t.get("cadernos", []):
                                            t["cadernos"].remove(caderno_remover)

                                    dados["tarefas"] = [
                                        t
                                        for t in dados["tarefas"]
                                        if len(t.get("cadernos", [])) > 0
                                    ]

                                    if dados["caderno_ativo"] == caderno_remover:
                                        dados["caderno_ativo"] = dados["cadernos"][0]
                                    if salvar_dados(dados):
                                        mostrar_feedback("Caderno removido!", "sucesso")
                            else:
                                mostrar_feedback("Número inválido!", "erro")
                        except:
                            mostrar_feedback("Entrada inválida!", "erro")

                elif sub_comando == "q":
                    break

        # Adicionar Tarefa
        elif comando == "+":
            print(f"\n{Cor.VERDE_B}➕ NOVA TAREFA{Cor.RESET}")
            print(f"{Cor.DIM}{'─' * 50}{Cor.RESET}")
            txt = input(f"Descrição: ").strip()
            if txt:
                try:
                    prior = input(
                        f"Prioridade ({Cor.VERMELHO_B}1{Cor.RESET}=Alta, {Cor.AMARELO_B}2{Cor.RESET}=Média, {Cor.VERDE_B}3{Cor.RESET}=Baixa) [{Cor.AMARELO_B}2{Cor.RESET}]: "
                    ).strip()
                    prior = int(prior) if prior else 2
                    prior = min(max(prior, 1), 3)
                except:
                    prior = 2

                # Criar lista de cadernos para a tarefa
                cadernos_tarefa = [dados["caderno_ativo"]]

                # Perguntar se quer adicionar em outros cadernos
                outros_cadernos = [
                    c for c in dados["cadernos"] if c != dados["caderno_ativo"]
                ]

                if outros_cadernos:
                    print(
                        f"\n{Cor.CIANO}Deseja adicionar esta tarefa em outros cadernos também?{Cor.RESET}"
                    )
                    print(f"{Cor.DIM}{'─' * 50}{Cor.RESET}")

                    for i, caderno in enumerate(outros_cadernos, 1):
                        print(f"  {i}. {caderno}")

                    print(
                        f"\n{Cor.DIM}Digite os números separados por vírgula (ex: 1,3) ou Enter para pular{Cor.RESET}"
                    )
                    escolhas = input(f"{Cor.CIANO}Cadernos:{Cor.RESET} ").strip()

                    if escolhas:
                        try:
                            indices = [int(x.strip()) - 1 for x in escolhas.split(",")]
                            for idx in indices:
                                if 0 <= idx < len(outros_cadernos):
                                    caderno_adicional = outros_cadernos[idx]
                                    if caderno_adicional not in cadernos_tarefa:
                                        cadernos_tarefa.append(caderno_adicional)
                        except:
                            print(
                                f"{Cor.AMARELO}⚠ Entrada inválida, tarefa criada apenas no caderno atual{Cor.RESET}"
                            )
                            input(f"{Cor.DIM}Pressione ENTER...{Cor.RESET}")

                dados["tarefas"].append(
                    {
                        "id": dados["proximo_id"],
                        "texto": txt,
                        "status": "•",
                        "caderno": dados["caderno_ativo"],
                        "cadernos": cadernos_tarefa,
                        "prioridade": prior,
                    }
                )
                dados["proximo_id"] += 1
                if salvar_dados(dados):
                    msg = "Tarefa adicionada com sucesso!"
                    if len(cadernos_tarefa) > 1:
                        msg += f" (em {len(cadernos_tarefa)} cadernos)"
                    mostrar_feedback(msg, "sucesso")

        # Concluir/Desconcluir Tarefa
        elif comando == "x":
            try:
                id_tarefa = int(input(f"\n{Cor.AMARELO}ID da tarefa:{Cor.RESET} "))
                for t in dados["tarefas"]:
                    if t["id"] == id_tarefa:
                        t["status"] = "X" if t["status"] == "•" else "•"
                        status_msg = "concluída" if t["status"] == "X" else "reaberta"
                        if salvar_dados(dados):
                            mostrar_feedback(f"Tarefa {status_msg}!", "sucesso")
                        break
                else:
                    mostrar_feedback("Tarefa não encontrada!", "erro")
            except:
                mostrar_feedback("ID inválido!", "erro")

        # Deletar Tarefa
        elif comando == "d":
            try:
                id_tarefa = int(
                    input(f"\n{Cor.VERMELHO}ID da tarefa para deletar:{Cor.RESET} ")
                )
                tarefa = next(
                    (t for t in dados["tarefas"] if t["id"] == id_tarefa), None
                )
                if tarefa:
                    confirma = input(
                        f"Confirma deletar '{tarefa['texto']}'? (s/n): "
                    ).lower()
                    if confirma == "s":
                        dados["tarefas"] = [
                            t for t in dados["tarefas"] if t["id"] != id_tarefa
                        ]
                        if salvar_dados(dados):
                            mostrar_feedback("Tarefa deletada!", "sucesso")
                else:
                    mostrar_feedback("Tarefa não encontrada!", "erro")
            except:
                mostrar_feedback("ID inválido!", "erro")

        # Editar Tarefa
        elif comando == "e":
            try:
                id_tarefa = int(
                    input(f"\n{Cor.AZUL}ID da tarefa para editar:{Cor.RESET} ")
                )
                for t in dados["tarefas"]:
                    if t["id"] == id_tarefa:
                        print(f"{Cor.DIM}Texto atual: {t['texto']}{Cor.RESET}")
                        novo_texto = input(f"Novo texto (Enter para manter): ").strip()
                        if novo_texto:
                            t["texto"] = novo_texto
                            if salvar_dados(dados):
                                mostrar_feedback("Tarefa editada!", "sucesso")
                        break
                else:
                    mostrar_feedback("Tarefa não encontrada!", "erro")
            except:
                mostrar_feedback("ID inválido!", "erro")

        # Alterar Prioridade
        elif comando == "p":
            try:
                id_tarefa = int(input(f"\n{Cor.AZUL}ID da tarefa:{Cor.RESET} "))
                nova_prior = int(
                    input(
                        f"Nova prioridade ({Cor.VERMELHO_B}1{Cor.RESET}=Alta, {Cor.AMARELO_B}2{Cor.RESET}=Média, {Cor.VERDE_B}3{Cor.RESET}=Baixa): "
                    )
                )
                for t in dados["tarefas"]:
                    if t["id"] == id_tarefa:
                        t["prioridade"] = min(max(nova_prior, 1), 3)
                        if salvar_dados(dados):
                            mostrar_feedback("Prioridade atualizada!", "sucesso")
                        break
                else:
                    mostrar_feedback("Tarefa não encontrada!", "erro")
            except:
                mostrar_feedback("Entrada inválida!", "erro")

        # Novo Caderno
        elif comando == "n":
            print(f"\n{Cor.AZUL_B}📚 NOVO CADERNO{Cor.RESET}")
            print(f"{Cor.DIM}{'─' * 50}{Cor.RESET}")
            novo_c = input(f"Nome: ").strip().title()
            if novo_c:
                if novo_c in dados["cadernos"]:
                    mostrar_feedback("Já existe um caderno com esse nome!", "aviso")
                else:
                    dados["cadernos"].append(novo_c)
                    if salvar_dados(dados):
                        mostrar_feedback(f"Caderno '{novo_c}' criado!", "sucesso")

        # Remover Caderno
        elif comando == "r":
            if len(dados["cadernos"]) <= 1:
                mostrar_feedback("Você precisa ter pelo menos um caderno!", "aviso")
            else:
                print(f"\n{Cor.VERMELHO}🗑️  REMOVER CADERNO{Cor.RESET}")
                print(f"{Cor.DIM}{'─' * 50}{Cor.RESET}")
                for i, c in enumerate(dados["cadernos"], 1):
                    n_tarefas = len(
                        [
                            t
                            for t in dados["tarefas"]
                            if c in t.get("cadernos", [t["caderno"]])
                        ]
                    )
                    print(f"  {i}. {c} ({n_tarefas} tarefas)")

                try:
                    idx = int(input(f"\nNúmero do caderno: ")) - 1
                    if 0 <= idx < len(dados["cadernos"]):
                        caderno_remover = dados["cadernos"][idx]

                        confirma = input(
                            f"\n{Cor.AMARELO}Remover '{caderno_remover}'? (As tarefas serão removidas apenas deste caderno) (s/n):{Cor.RESET} "
                        ).lower()
                        if confirma == "s":
                            dados["cadernos"].pop(idx)

                            # Remover o caderno da lista de cadernos de cada tarefa
                            for t in dados["tarefas"]:
                                if caderno_remover in t.get("cadernos", []):
                                    t["cadernos"].remove(caderno_remover)

                            # Remover tarefas que ficaram sem cadernos
                            dados["tarefas"] = [
                                t
                                for t in dados["tarefas"]
                                if len(t.get("cadernos", [])) > 0
                            ]

                            if dados["caderno_ativo"] == caderno_remover:
                                dados["caderno_ativo"] = dados["cadernos"][0]
                            if salvar_dados(dados):
                                mostrar_feedback("Caderno removido!", "sucesso")
                    else:
                        mostrar_feedback("Número inválido!", "erro")
                except:
                    mostrar_feedback("Entrada inválida!", "erro")

        # Gerenciar Metas
        elif comando == "m":
            gerenciar_metas(dados)

        # Notas Rápidas
        elif comando == "a":
            gerenciar_notas(dados)

        # Registrar atividade no heatmap
        elif comando == "h":
            registrar_atividade_diaria(dados)

        # Estatísticas
        elif comando == "s":
            mostrar_estatisticas_gerais(dados)

        # Sair
        elif comando == "q":
            limpar_tela()
            print(f"\n{Cor.CIANO_B}{'━' * 60}{Cor.RESET}")
            print(f"{Cor.BOLD}{Cor.CIANO_B}{'👋 Até logo!'.center(60)}{Cor.RESET}")
            print(
                f"{Cor.DIM}{'Seus dados foram salvos com sucesso.'.center(60)}{Cor.RESET}"
            )
            print(f"{Cor.CIANO_B}{'━' * 60}{Cor.RESET}\n")
            break


if __name__ == "__main__":
    main()
