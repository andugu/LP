# Generated from Enquestes.g by ANTLR 4.7.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .EnquestesParser import EnquestesParser
else:
    from EnquestesParser import EnquestesParser

# This class defines a complete generic visitor
# for a parse tree produced by EnquestesParser.


class EnquestesVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by EnquestesParser#root.
    def visitRoot(self, ctx: EnquestesParser.RootContext):
        # Retorna una llista amb tota la informacio necessaria per fer un graf
        Header = ["E"]
        Links = ["LINKS"]
        Alternatives = []
        Preguntes = []
        Respostes = []

        c = [x for x in ctx.getChildren()]
        for i in c:

            T = self.visit(i)

            if T is not None:
                if T[0] == "LLISTA":
                    for j in range(1, len(T)):
                        Header.append(T[j])
                    Header.append("END")

                elif T[0] == "LINK":
                    for j in range(1, len(T)):
                        Links.append(T[j])

                elif T[0] == "ALTERNATIVA":
                    for j in range(0, len(T)):
                        Alternatives.append(T[j])

                elif T[0] == "PREGUNTA":
                    for j in range(0, len(T)):
                        Preguntes.append(T[j])

                elif T[0] == "RESPOSTA":
                    for j in range(0, len(T)):
                        Respostes.append(T[j])

        return Header+Links+Alternatives+Preguntes+Respostes

    # Visit a parse tree produced by EnquestesParser#entrada.
    def visitEntrada(self, ctx: EnquestesParser.EntradaContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by EnquestesParser#identificador.
    def visitIdentificador(self, ctx: EnquestesParser.IdentificadorContext):
        i = next(ctx.getChildren()).getText()
        return i

    # Visit a parse tree produced by EnquestesParser#numero.
    def visitNumero(self, ctx: EnquestesParser.NumeroContext):
        i = int(next(ctx.getChildren()).getText())
        return str(i)

    # Visit a parse tree produced by EnquestesParser#pregunta.
    def visitPregunta(self, ctx: EnquestesParser.PreguntaContext):
        # Retorna nomes el identificador
        c = [x for x in ctx.getChildren()]
        return ["PREGUNTA"]+[self.visit(c[0])]+[self.visit(c[3])]

    # Visit a parse tree produced by EnquestesParser#contingut.
    def visitContingut(self, ctx: EnquestesParser.ContingutContext):
        c = [x for x in ctx.getChildren()]
        S = ""
        for i in range(0, len(c)):
            S += c[i].getText()
            if i < len(c)-1:
                S += " "
        return S

    # Visit a parse tree produced by EnquestesParser#resposta.
    def visitResposta(self, ctx: EnquestesParser.RespostaContext):
        # Retorna el identifiacador de la resposta i els numeros de la resposta
        c = [x for x in ctx.getChildren()]
        L = []
        for i in range(3, len(c)):
            L.append(self.visit(c[i]))
        return ["RESPOSTA"]+[self.visit(c[0])]+L

    # Visit a parse tree produced by EnquestesParser#respostes.
    def visitRespostes(self, ctx: EnquestesParser.RespostesContext):
        # Retorna el numero de la resposta i el contingut
        c = [x for x in ctx.getChildren()]
        return [self.visit(c[0])]+[self.visit(c[2])]

    # Visit a parse tree produced by EnquestesParser#link.
    def visitLink(self, ctx: EnquestesParser.LinkContext):
        # Retorna els ID del link, i els de pregunta -> resposta
        c = [x for x in ctx.getChildren()]
        L = [c[0].getText(), c[3].getText(), c[5].getText()]
        return ["LINK"]+L

    # Visit a parse tree produced by EnquestesParser#alternativa.
    def visitAlternativa(self, ctx: EnquestesParser.AlternativaContext):
        # Retorna una llista de subllistes de les alternatives
        # (que tambe es subllista)
        L = []
        c = [x for x in ctx.getChildren()]
        for i in range(3, len(c)):
            for j in self.visit(c[i]):
                L.append(j)
        return L

    # Visit a parse tree produced by EnquestesParser#alternatives.
    def visitAlternatives(self, ctx: EnquestesParser.AlternativesContext):
        c = [x for x in ctx.getChildren()]
        # Visitem nomes el identificador i les parelles
        L = ["ALTERNATIVA"]
        L.append(self.visit(c[0]))
        for i in self.visit(c[2]):
            L.append(i)
        return L

    # Visit a parse tree produced by EnquestesParser#pairs.
    def visitPairs(self, ctx: EnquestesParser.PairsContext):
        c = [x for x in ctx.getChildren()]
        # Retornem una llista de subllistes de parelles
        L = []
        for i in c:
            a = self.visit(i)
            if a is not None:
                for r in a:
                    L.append(r)
        return L

    # Visit a parse tree produced by EnquestesParser#pair.
    def visitPair(self, ctx: EnquestesParser.PairContext):
        c = [x for x in ctx.getChildren()]
        # Retornem el numero i el identificador
        return [self.visit(c[0]), self.visit(c[2])]

    # Visit a parse tree produced by EnquestesParser#llista.
    def visitLlista(self, ctx: EnquestesParser.LlistaContext):
        # Retorna la llista de preguntes
        L = []
        c = [x for x in ctx.getChildren()]
        for i in range(1, len(c)):
            L.append(self.visit(c[i]))
        return ["LLISTA"]+L


del EnquestesParser
