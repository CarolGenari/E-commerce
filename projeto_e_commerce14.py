"""
-Salvando e Pagando o pedido:

-A primeira verificação que temos que fazer é perceber se quando o cliente for
fazer o pagamento, se existe estoque suficiente d eum produto, na base de dados
-Para isso, temos que ir no arquivo views, da app pedido:
    -Vamos fazer as alterações na class Pagar
    -Vamos já retornar o arquivo criado anteriormente e que está dnetro da pasta
    templates da app: 'pagar.html'
    -Na class, definimos o template name e o método get
    -Depois demos um return render
    -Agora vamos abrir o arquivo 'pagar.html', extender o base.html e criar
    um bloco de conteúdo para vermos se isso já está sendo renderizado
    -Agora, faremos algumas verificações. Elas tbm serão feitas nessa class 
    Pagar. A primeira que faremos será verificar se o usuário está logado. Se
    ele não possuir um cadastro, já vamos redirecioná-lo para que crie um perfil:
            if not self.request.user.is_authenticated:
                return redirect('perfil:criar')
    -Outra verificação será se o carirnho possui produtos:
            if not self.request.session.get('carrinho'):
                return redirect('produto:lista')
    -Próxima verifcação: ver se a variação e produto escolhidos pelo cliente 
    tem estoque disponível na base de dados. Pra pegarmos as variações vamos
    usar seus ids, lembrando que esses são as keys. Para isso, primeiro pegamos
    o carrinho: carrinho = self.request.session.get('carrinho') e depois vamos
    iterar sobre esses ids: carrinho_variacao_ids = [v for v in carrinho]. Agora
    vamos precisar selecionar todas essas varições que estão no carrinho, na 
    base de dados. Temos que importar: from produto.models import Variacao e aí
    sim vamos selecionar essas variações lá da base de dados: 
            bd_variacoes = list(
            Variacao.objects.select_related('produto').filter(
                id__in=carrinho_variacao_ids)
        )
        -Obs: aqui já vamos converter tbm em uma lista
        -Obs: esse selected_related('produto') estamos usando para dimunir o
        nº de consultas que estão sendo realizadas na página. O Django agora 
        está fazendo essas consultas dentro de produto
-Agora já podemos começar a percorrer essas variações e saber se existem variações
e produtos disponíveis em estoque, para que o cliente possa realizar sua compra:
        for variacao in bd_variacoes:
            vid = str(variacao.id)

            estoque = variacao.estoque
            qtd_carrinho = carrinho[vid]['quantidade']
            preco_unt = carrinho[vid]['preco_unitario']
            preco_unit_promo = carrinho[vid]['preco_unitario_promocional']
    -Já pegamos todas as variáveis que são necessárias e agora temos que fazer 
    a checagem: 
             if estoque < qtd_carrinho:
                carrinho[vid]['quantidade'] = estoque
                carrinho[vid]['preco_quantitativo'] = estoque * preco_unt
                carrinho[vid]['preco_quantitativo_promo'] = estoque * \
                    preco_unit_promo
        -Temos que alterar os preços, consoante o estoque disponível
        -Depois, adicionamos uma mensagem para o cliente e não podemos de esquecer
        de salvar e depois redirecionar o clienye para o carrinho
            if error_msg_estoque:
                messages.error(
                    self.request,
                    error_msg_estoque

                )
                self.request.session.save()
                return redirect('produto:carrinho')
        -Com isso, já conseguimos garantir que o cliente não vai comprar produtos
        que não estejam em estoque.

-Vamos agora olhar para o arquivo models da app pedido:
    -Fizemos uma pequena alteração no models, adicionando uma nova variável na
    na class Pedido ( qtd_total = models.PositiveIntegerField()). Agora temos 
    que fazer as migrações (makemigrations e depois o migrate)
    -Agora já podemos usar essa variável lá no views
    -Vamos tbm precisar do arquivo utils, onde temos as funções que definimos
    -Vamos tbm precisar importar o Pedido e ItemPedido, as 2 class que estão 
    no arquivo models da app pedido, para o arquivo views e depois já vamos 
    mandar as variáveis relacionadas ao pedido, que estavam definidas no models
    -Assim, já fazemos o registro do pedido:
        pedido = Pedido(
            usuario=self.request.user,
            total=valor_total_carrinho,
            qtd_total=qtd_total_carrinho,
            status='C',
        )
    -Agora, vamos criar um bulk_create, que é uma criação em massa. A criação 
    de dados em massa retorna o que o banco de dados retorna: o número de 
    registros criados: 
            ItemPedido.objects.bulk_create(
                [
                    ItemPedido(
                        pedido=pedido,
                        produto=v['produto_nome'],
                        produto_id=v['produto_id'],
                        variacao=v['variacao_nome'],
                        variacao_id=v['variacao_id'],
                        preco=v['preco_quantitativo'],
                        preco_promocional=v['preco_quantitativo_promocional'],
                        quantidade=v['quantidade'],
                        imagem=v['imagem'],
                    ) for v in carrinho.values()
                ]
            )

-Obs: algumas modificações que ficaram por fazer
    -No arquivo urls.py da app pedido, tínhamos adicionado a utl 'lista' e agora
    vamos ajeitar a primeira url, que é pagar
    -Depois, vamos no views e vamos mover o que tinhamos feito na class Pagar
    para a class SalvarPedido. Assim, depois do pedido ser salvo, vamos redirecionar
    para Pagar
    -Então, a Class SalvarPedido não vai ter umtemplate, ela servirá apenas para
    realizar sua tarefa e depois vamos para Pagar
    -Nas urls, em 'pagar', ela deverá receber uma primary-key <int:pk>, porque
    ela terá que conseguir abrir um pedido de acordo com seu id
    -Então, moveremos todo o código que está dentro da class Pagar para a class
    SalvarPedido
    -Como trocamos esse código de classe, temos que alterar isso tbm no arquivo
    'resumodacompra.html', que está dnetro da pasta templates da app produto.
    Na parte do html que correspondia a Realizar pedido e pagar, estava 
    href="{% url 'pedido:pagar' %}" e devemos alterar para: 
    href="{% url 'pedido:salvarpedido' %}"
    -Assim que fizemos essa mudança, já fizemos o commit para o GitHub
    -Não podemos esquecer que quando o carrinho é salvo, em SalvarPedido, ele
    já é eliminado: del self.request.session['carrinho']

-Agora, na class SalvarPedido ainda temos que adicionar o código que corresponde
ao redirecionamento de página, para que o cliente possa pagar. Vamos selecionar
o pedido para pagamento através do seu id(primary-key): 
        return redirect(
            reverse(
                'pedido:pagar',
                kwargs={
                    'pk': pedido.pk
                }
            )
        )

-No arquivo views, vamos importar o DetailView e a class Pagar vai herdar dela
e vamos dar coninuidade as edições dessa class Pagar:
    -Vamos adicionar o template_name mais algumas variáveis
    -Depois vamos pegar parte do código que está dentro de um arquivo que ele
    nos enviou, chamado 'pagar.html' e vamos adicionar dentro do nosso arquivo
    'pagar.html', que está dentro da app pedido
    -Pegamos a parte do código que estava entre a tag <main> e colocamos no
    nosso arquivo pagar.html, dentro do conteudo e vamos começar as alterações
    necessárias

-Obs: conseguimos abrir a página final, antes do pagamento, onde se tem os dados
do pedido, através de uma guia anónima. Isso não pode acontecer por motivos de
segurança. Para isso, faremos o seguinte:
    -No arquivo views, criaremos uma class DispatchLoginRequired(View). Depois,
    dentro dessa class, vamos definir o método dispatch que descobre para onde
    a página está indo (se é POST ou GET). Esse método está dentro dessa class
    View e nós vamos modificá-lo. Vamos criar uma condicional para verificar se
    o usuário está autenticado. Se ele não estiver, vamos redirecioná-lo para
    a página de login ('perfil:criar')
    -Obs: não podemos esquecer de colocar essa class DispatchLoginRequired como
    herança na class Pagar

-Obs: temos outro problema por resolver. Outro cliente conseguiria aceder a um
carrinho de compras de outro cliente, nessa fase de escolha de pagamento, através
do nº do pedido. Isso tbm não pode acontecer.
    -Na class Pagar, vamos definir o método queryset() e vamos filtrar essa
    queryset pelo usuário que estiver logado, ou seja, cada usuário terá acesso
    apenas ao seu carrinho e método de pagamento, através do seu login:
        def get_queryset(self, *args, **kwargs):
            qs = super().get_queryset(*args, **kwargs)
            qs = qs.filter(usuario=self.request.user)
            return qs

-No arquivo views da app pedido ainda está faltando configurar a class Detalhe
e a class Lista. Uma será o complemento da outra. Vamos ter uma lista de pedidos
de um cliente e quando entrarmos nessa lista, vão aparecer os detalhes

"""
