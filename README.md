# Jogo de Advinhação com Machine Learning

Este projeto tem como objetivo criar um jogo de adivinhação muito semelhante ao [Akinator](https://pt.akinator.com/), em que caracteristicas são informadas pelo usuário e com base nessas informações um personagem do seriado Os Simpsons é mostrado.

![Janela Principal](https://github.com/lynconEBB/AkinatorPython/blob/master/Imagens/exemplos/principal.png)

---

### Requisitos

- Pyhton 3+
- Pip

### Considerações

O programa só foi testado em sistemas operacionais linux, é provável que também funcione em outros sistemas operacionais necessitando de algumas modificações.

Este projeto foi desenvolvido como atividade avaliativa na disciplina de Topicos Especiais do curso de Informática do Instituto Federal do Paraná.

### Instalação

Primeiramente clone o repositório no local em que achar adequado com o comando:
```bash
git clone https://github.com/lynconEBB/AkinatorPython
```
Em seguida, instale as dependencias necessárias utilizando o seguinte comando estando na pasta raiz do projeto:
```bash
pip3 install -r requirements.txt
```
Por fim, instale os programas eog e graphviz utilzando o gerenciador de pacotes da sua distribuição linux
```bash
sudo apt install eog
sudo apt install graphviz
```
### Uso
Para iniciar o programa execute o arquivo [front.py](https://github.com/lynconEBB/AkinatorPython/blob/master/src/front.py), estando na pasta raiz o comando para executar é:
```bash
python3 src/front.py
```
Com isso o programa será executado e janela principal será exibida, nela é possivel selecionar as caracteristicas do personagem que está pensando e clicando no botão adivinhar, caso o programa encontre o personagem ele será exibido.

É possível também adicionar um personagem que não esteja no banco de dados do programa clicando no botão de adicionar na barra lateral, assim que clicado uma nova janela para realizar esta ação.

![Janela Adicionar Personagem](https://github.com/lynconEBB/AkinatorPython/blob/master/Imagens/exemplos/addPersonagem.png)

Além disso, ao clicar no outro botão da barra lateral é possivél visualizar a árvore de decisões que o programa utiliza para realizar as adivinhações.

![Arvore de Decisões](https://github.com/lynconEBB/AkinatorPython/blob/master/Imagens/exemplos/arvoreDecisao.png)

### Licença

[MIT](https://github.com/lynconEBB/AkinatorPython/blob/master/LICENSE)