"""
-Corrigindo Títulos

-Até agora, o que falta fazer nesse projeto:
    -Na página de Resumo da Compra: ajustar títulos, CPF único e Criar a Busca
    -Podemos tbm já remover o Debug Toolbar

-A primeira coisa que faremos é remover o Debug Toolbar. Eu não vou retirar do
meu projeto, mas o passo-a-passo é:
    -Ir no arquivo urls.py do projeto principal (loja) e retirar o #TODO que lá
    está 
    -Depois, no arquivo settings.py do projeto principal temos que removê-lo 
    do INSTALLED_APPS e lá na final do arquivo tem a parte do INTERNAL_IPS para
    remover tbm. Não esquecer de remover do MIDDLEWARE

-Agora vamos corrigir os títulos das páginas:
    -Isso fazemos sempre nos templates
    -Começando pelo arquivo 'base.html'
    -Depois temos que ir alterando todos os arquivos, de todas as apps, que 
    pertençam aos templates

-CPF único:
    -Arquivo models da app perfil
    -Já estávamos fazendo algumas validações no método clean()
    -Vamos definir agora: cpf_enviado = self.cpf or None
                          cpf_salvo = None
                          perfil = Perfil.objects.filter(cpf=cpf_enviado).first()
    -Agora temos que checar se o usuário tem registro e se o cpf encontrado na
    base de dados é daquele perfil. Existe a possibilidade de encontrar um cpf 
    na base de dados que pertença a outro perfil e isso vai gerar erro:
            if cpf_salvo is not None and self.pk != perfil.pk:
                 error_messages['cpf'] = 'CPF já existe.'

-Criando a busca:
    -


"""
