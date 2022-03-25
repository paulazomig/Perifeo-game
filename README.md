#Implementação do jogo Perifero

Esse repositório contém a implementação do jogo Perifero.
O jogo é composto por um tabuleiro com 25 peças hexagonais, com duas de suas bordas pretas e duas amarelas.
O objetivo do jogo é conectar dois lados opostos do tabuleiro por uma sequencia contínua de peças, sendo as peças da mesma cor que os lados conectados. 

Regras do jogo:
- Cada jogador deverá jogar com as peças de seu oponente;
- O jogo é iniciado pelo jogador de cor preta. Ele irá jogar com peças amarelas;
- Os jogadores devem intercalar seus turnos;
- A cada jogada uma nova peça deve ser inserida no tabuleiro. As peças podem ser inseridas apenas pelas casas localizadas nas bordas do tabuleiro;
- Para inserir uma nova peça no tabuleiro, pode ser necessário empurrar as peças já existentes. Só podem ser empurradas  as peças que estão em uma linha reta a partir da casa de entrada da nova peça no tabuleiro. As peças podem ser empurradas para apenas uma casa adjacente, sem alterar sua ordem. 
- Não é permitido realizar uma jogada que resultará em uma peça ser empurrada para fora do tabuleiro
- O jogo é finalizado quando os dois lados de uma cor são conectados por uma corrente de peças daquela mesma cor. Não importa qual jogador realizar a jogada final, o vencedor é aquele que teve seus dois lados conectados.

Para selecionar a casa do tabuleiro onde a peça será inserida deve-se clicar na casa desejada.
Para empurrar peças em alguma direção são necessários dois cliques: Um na casa onde a nova peça será inserida e um em um hexágono adjacente, para definir a direção em que as peças devem ser empurradas. 
O jogo deve ser executado a partir da classe Tabuleiro.