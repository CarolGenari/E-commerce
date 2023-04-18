"""
-Lista e Detalhe do Pedido para o usuário:

-Nessa aula, faremos a parte da lista dos pedidos de um usuário e tbm os detalhes
dessas listas
-Como as classes Lista e Detalhes tbm vão ter que ter aquele método queryset
que definimos anteriormente, vamos mudá-lo de lugar. Vamos tirá-lo da class
Pagar e vamos colocá-lo na class DispatchLoginRequired. A única questão é, para
não gerar erro, teremos que colocar essa class como Mixin, porque a class View,
da qual essa class herda, não possui esse método queryset

-Começaremos então pela class Lista:
    -Ela herdará de (DispatchLoginRequiredMixin) e tbm de LisView
    -Isso já vai restringir o acesso para apenas usuários logados
    -Vamos definir o model da classe, o context_object_name, o template name.
    -Lembrando que após definir o template name, temos que criar o arquivo com
    o mesmo nome dentro da pasta templates da app pedido. No caso, o nome do
    arquivo é 'lista.html'
    -Agora, nesse arquivo criado, já podemos extender o arquivo 'base.html' e
    criar o block do conteúdo
    -Vamos adicionar essa opção de 'meus pedidos' na navbar
    -Agora, o que temos que fazer é renderizar o conteúdo
    -Ele nos enviou o arquivo 'pedidos.html' já com o código html que será 
    necessário. Pegamos a parte do código que está dentro da tag <main>
    -As alterações já foram feitas, agora temos que ajeitar a parte dos Detalhes
    da encomenda

-Agora, faremos as alterações na class Detalhe:
    -Essa classe vai herdar de: DispatchLoginRequiredMixin, DetailView
    Dentro do arquivo 'pagar.html' que está dentro de templates da app pedido,
    vamos retirar uma parte do código, vamos colocá-la dentro de um arquivo
    chamado '_pedido.html' que criaremos dentro da pasta templates -» parciais
    -Não esquecer de colocar o {% include 'parciais/_pedido.html' %} de onde
    esse código foi tirado, do arquivo pagar.html
    -Agora, vamos editar o arquivo detalhe.html da app pedido, para decidirmos
    o que será exibido nos detalhes de uma encomenda. Basicamente será exibido
    o que já está sendo exibido no pedido do cliente. Por isso incluímos o
    parcial: _pedido.html nesse arquivo

"""
