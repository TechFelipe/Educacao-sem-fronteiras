# Diagrama de classes do domínio

```mermaid
classDiagram
    class Usuario {
      +int id
      +str nome
      +str email
      +str senha
      +salvar()
      +atualizar()
      +deletar()
      +listar_todos()
      +buscar_por_id()
    }
    class Tema {
      +int id
      +str titulo
      +str descricao
      +str dificuldade
      +datetime criado_em
      +salvar()
      +atualizar()
      +deletar()
      +listar_todos()
      +buscar_por_id()
    }
    class Redacao {
      +int id
      +int usuario_id
      +int tema_id
      +str texto
      +int nota_total
      +datetime data_envio
      +salvar()
      +atualizar()
      +deletar()
    }
    class NotaCompetencia {
      +int id
      +int redacao_id
      +int competencia1
      +int competencia2
      +int competencia3
      +int competencia4
      +int competencia5
      +salvar()
      +atualizar()
      +deletar()
    }
    Usuario "1" --> "0..*" Redacao : escreve
    Tema "1" --> "0..*" Redacao : tema escolhido
    Redacao "1" *-- "0..*" NotaCompetencia : possui notas
```

`Usuario`, `Tema`, `Redacao` e `NotaCompetencia` herdam de `db.Model`. A relação entre `Redacao` e `NotaCompetencia` usa composição lógica: as notas dependem da redação e são removidas junto com ela.
