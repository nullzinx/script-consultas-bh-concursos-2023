<div align="center">

# 🔎📄 BH Concursos 2023 Scraper

**Consulta de candidatos na lista geral de resultados do concurso de 2023 da Câmara Municipal de Belo Horizonte, direto pela linha de comando.**

![Python](https://img.shields.io/badge/Python-3-3776AB?logo=python&logoColor=white)
![httpx](https://img.shields.io/badge/httpx-requisições_HTTP-0B7285)
![Beautiful Soup](https://img.shields.io/badge/BeautifulSoup4-HTML_parsing-2F9E44)
![pypdf](https://img.shields.io/badge/pypdf-leitura_de_PDF-D9480F)
![CLI](https://img.shields.io/badge/interface-CLI_(argparse)-495057)
![Regex](https://img.shields.io/badge/extração-expressão_regular-7048E8)

[Sobre](#-sobre-o-projeto) •
[Funcionalidades](#-funcionalidades) •
[Instalação](#-instalação) •
[Como utilizar](#-como-utilizar) •
[Limitações](#-limitações-conhecidas) •
[Aviso legal](#-aviso-legal)

</div>

---

## 📌 Sobre o projeto

O **BH Concursos 2023 Scraper** é um script Python de arquivo único que:

1. acessa a página oficial de resultados do concurso de 2023 da Câmara Municipal de Belo Horizonte (CMBH);
2. localiza o link do PDF **"Resultado final - todos os cargos (Lista geral)"**;
3. baixa o PDF, percorre suas páginas e procura o nome informado pelo usuário;
4. tenta extrair os dados do candidato por meio de uma expressão regular e imprime o resultado no terminal.

> ⚠️ **Importante:** a extração depende da estrutura textual do PDF e da expressão regular utilizada. Se o layout do documento mudar, ou se o texto extraído pelo `pypdf` vier com espaçamento diferente do esperado, o candidato pode não ser encontrado mesmo constando no PDF. Veja as [limitações conhecidas](#-limitações-conhecidas).

---

## ✨ Funcionalidades

- Recebe o nome do candidato pela linha de comando (`-q` / `--query`).
- Acessa a página de resultados da CMBH e localiza o link do PDF da lista geral pelo texto do link.
- Baixa o PDF em memória (sem salvá-lo em disco) e lê o texto página por página.
- Busca o nome sem diferenciar maiúsculas de minúsculas.
- Extrai, via expressão regular, os campos: inscrição, nome, prova objetiva, prova discursiva, data de nascimento, situação, cota, classificação e nota final.
- Informa o número da página do PDF em que o candidato foi encontrado.
- Imprime o resultado como um dicionário Python (`print(result)`).

---

## 🧰 Tecnologias utilizadas

| Tecnologia | Uso no projeto | Documentação |
|---|---|---|
| **Python 3** | Linguagem do script | [docs.python.org](https://docs.python.org/3/) |
| **httpx** | Requisições HTTP (página de resultados e PDF) | [python-httpx.org](https://www.python-httpx.org/) |
| **Beautiful Soup 4** | Análise do HTML para localizar o link do PDF | [Documentação](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) |
| **pypdf** | Leitura do PDF e extração de texto | [pypdf.readthedocs.io](https://pypdf.readthedocs.io/) |
| **argparse** *(biblioteca padrão)* | Argumentos de linha de comando | [Documentação](https://docs.python.org/3/library/argparse.html) |
| **re** *(biblioteca padrão)* | Expressão regular de extração | [Documentação](https://docs.python.org/3/library/re.html) |
| **io.BytesIO** *(biblioteca padrão)* | Leitura do PDF diretamente da memória | [Documentação](https://docs.python.org/3/library/io.html#io.BytesIO) |

---

## 📋 Requisitos

- Python 3 instalado.
- Acesso à internet (o script consulta o site da CMBH a cada execução).
- Bibliotecas de terceiros: `httpx`, `beautifulsoup4` e `pypdf`.

---

## ⚙️ Instalação

Clone o repositório (substitua pela URL do seu repositório) e entre na pasta:

```bash
git clone <url-do-repositorio>
cd <pasta-do-repositorio>
```

*(Opcional, recomendado)* Crie e ative um ambiente virtual:

```bash
python -m venv .venv

# Linux / macOS
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

Instale as dependências:

```bash
pip install httpx beautifulsoup4 pypdf
```

---

## 🚀 Como utilizar

Execute o script informando o nome do candidato com `-q` ou `--query`:

```bash
python bh-concursos-2023-scrapper.py -q "nome do candidato"
```

ou, de forma equivalente:

```bash
python bh-concursos-2023-scrapper.py --query "nome do candidato"
```

### Argumentos

| Opção | Forma longa | Tipo | Obrigatório | Descrição |
|---|---|---|---|---|
| `-q` | `--query` | texto | ✅ Sim | Nome do candidato a ser procurado na lista geral. |

Para ver a ajuda gerada pelo `argparse`:

```bash
python bh-concursos-2023-scrapper.py -h
```

### 💡 Dicas de busca

- A comparação ignora maiúsculas/minúsculas e espaços nas extremidades do texto informado.
- A expressão regular espera o nome **completo**, exatamente como aparece no PDF (incluindo acentos).
- Nomes parcialmente digitados podem localizar a página, mas não serão extraídos pela expressão regular.

---

## 🖥️ Exemplos de saída

> 🧪 **Atenção:** todos os exemplos abaixo são **fictícios**, criados apenas para ilustrar o formato da saída. Nomes, números, datas e notas não correspondem a candidatos reais.

**Candidato encontrado:**

```text
{'found': True, 'candidate': {'inscricao': '12345678', 'nome': 'maria exemplo da silva', 'prova_objetiva': '40', 'prova_discursiva': '7,50', 'nascimento': '01/01/1990', 'situacao': 'aprovado', 'cota': None, 'classificacao': '10º', 'nota_final': '47,50', 'page': 3}}
```

**Candidato encontrado, com cota (`negro`):**

```text
{'found': True, 'candidate': {'inscricao': '87654321', 'nome': 'joao exemplo de souza', 'prova_objetiva': '38', 'prova_discursiva': '6,00', 'nascimento': '15/06/1985', 'situacao': 'aprovado', 'cota': 'negro', 'classificacao': '25º', 'nota_final': '44,00', 'page': 5}}
```

**Candidato não encontrado:**

```text
{'found': False}
```

**PDF não localizado na página de resultados:**

```text
{'found': False, 'error': 'PDF não encontrado na página'}
```

> ℹ️ O nome é retornado em letras minúsculas porque o texto do PDF é convertido para minúsculas antes da extração. O campo `cota` é `None` quando a cota não aparece no trecho analisado.

### Campos retornados

| Campo | Descrição |
|---|---|
| `found` | `True` se o candidato foi encontrado; `False` caso contrário. |
| `candidate` | Dicionário com os dados extraídos (presente apenas quando `found` é `True`). |
| `error` | Mensagem de erro (presente apenas quando o PDF não é localizado na página). |
| `inscricao` | Número de inscrição. |
| `nome` | Nome do candidato, em minúsculas. |
| `prova_objetiva` | Valor numérico da prova objetiva. |
| `prova_discursiva` | Valor da prova discursiva. |
| `nascimento` | Data de nascimento (`dd/mm/aaaa`). |
| `situacao` | `aprovado` ou `reprovado`. |
| `cota` | `negro`, quando presente; caso contrário, `None`. |
| `classificacao` | Classificação (ex.: `10º`). |
| `nota_final` | Nota final. |
| `page` | Número da página do PDF onde o candidato foi encontrado. |

---

## 🗂️ Estrutura do projeto

```text
.
├── bh-concursos-2023-scrapper.py   # Script principal (CLI)
└── README.md                       # Este documento
```

Funções do script:

| Função | Responsabilidade |
|---|---|
| `building_args()` | Define e processa os argumentos de linha de comando (`-q` / `--query`). |
| `scraping(query)` | Acessa a página, localiza e baixa o PDF, percorre as páginas e procura o candidato. |
| `extract_candidate(text, query)` | Aplica a expressão regular ao texto da página e devolve os campos extraídos. |

---

## 🚧 Limitações conhecidas

- **Dependência do layout do PDF:** a expressão regular assume uma ordem e um espaçamento específicos entre os campos (por exemplo, a data de nascimento logo após a nota da prova discursiva, e a nota final logo após a classificação). Qualquer mudança no texto extraído pode impedir a extração.
- **Nome completo e exato:** a expressão regular exige o nome inteiro, igual ao do PDF. Variações de grafia, acentuação ou espaçamento podem resultar em "não encontrado".
- **Valores de situação e cota limitados:** a expressão reconhece apenas `aprovado`/`reprovado` e a cota `negro`. Outras situações ou cotas, se existirem no PDF, não são previstas.
- **Localização do PDF por texto exato:** o link é encontrado pelo texto `Resultado final - todos os cargos (Lista geral)`. Se o texto do link mudar no site, o PDF não será localizado.
- **URL do PDF:** o script usa o valor do atributo `href` diretamente; não há tratamento para links relativos ou ausentes.
- **Sem tratamento de erros de rede:** falhas de conexão, status HTTP de erro ou *timeouts* não são tratados e interrompem o script com uma exceção. Nenhum *timeout* é configurado explicitamente.
- **Sem cache:** o PDF é baixado novamente a cada execução.
- **Primeira ocorrência:** a busca retorna apenas o primeiro resultado que satisfizer a expressão regular.
- **Texto extraído de PDF:** páginas sem texto extraível (por exemplo, imagens escaneadas) são ignoradas, pois não há OCR.
- **Sem testes automatizados** e sem garantias de funcionamento contínuo. Não há evidências, neste repositório, de que o projeto esteja pronto para uso em produção.

---

## 💡 Possíveis melhorias

- [ ] Tratar erros de rede e de resposta HTTP com mensagens amigáveis.
- [ ] Definir *timeout* e tentativas de nova requisição.
- [ ] Resolver links relativos do PDF.
- [ ] Permitir busca parcial ou normalizada de nomes (ignorando acentos e espaços extras).
- [ ] Tornar a expressão regular mais tolerante a variações de espaçamento e a outras situações/cotas.
- [ ] Oferecer saída formatada (por exemplo, JSON ou tabela) em vez de imprimir o dicionário.
- [ ] Manter cache local do PDF para evitar downloads repetidos.
- [ ] Adicionar testes automatizados e um arquivo de dependências (`requirements.txt`).
- [ ] Definir uma licença para o projeto.

---

## 🏛️ Fonte oficial dos dados

Os dados são obtidos da página oficial de resultados do concurso de 2023 da Câmara Municipal de Belo Horizonte:

🔗 <https://www.cmbh.mg.gov.br/transparencia/concursos/2023/resultados>

O documento utilizado é o PDF identificado no site como **"Resultado final - todos os cargos (Lista geral)"**. Para informações oficiais e definitivas, consulte sempre diretamente o site da CMBH.

---

## ⚖️ Aviso legal

Este é um projeto **independente** e **não possui qualquer afiliação, vínculo ou endosso** da Câmara Municipal de Belo Horizonte (CMBH) ou de qualquer órgão público.

O script apenas automatiza a consulta a informações publicadas na página oficial. Não há garantia de que os dados extraídos estejam completos, corretos ou atualizados; a extração pode falhar ou produzir resultados incorretos caso o formato do PDF mude. Os resultados **não substituem** a consulta ao documento oficial. Utilize por sua conta e risco e respeite os termos de uso e as políticas do site de origem.

---

<div align="center">

Feito para fins de estudo e automação de consultas públicas.

</div>
