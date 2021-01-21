grammar Enquestes;

root : entrada+ END EOF;

entrada : pregunta | resposta | link | alternativa | llista ;

identificador: ID;
numero: NUM;

pregunta: identificador DOSPUNTS 'PREGUNTA' contingut;
contingut: (STRING | ID)+;

resposta: identificador DOSPUNTS 'RESPOSTA' (respostes)+;
respostes: numero DOSPUNTS contingut (PUNTICOMA)*;

link: identificador DOSPUNTS 'ITEM' identificador '->' identificador;

alternativa: identificador DOSPUNTS 'ALTERNATIVA' alternatives+;
alternatives: identificador '['pairs']';
pairs: '(' pair ')' ( ',' '(' pair ')' )*;
pair: numero ',' identificador;

llista: 'E: ENQUESTA' identificador+;

WS: [ \n\t\r\f]+ -> skip;
COMENTARI_MULTIPLE: '/*' .*? '*/' -> skip;
COMENTARI_UNIC: '//' ~[\r\n]* -> skip;
END: 'END';
NUM: ([0-9])+;
ID: ([0-9] | [a-z] | [A-Z] | [\u0080-\u00FF])+;
STRING: (ID'?')+;
DOSPUNTS: ':';
PUNTICOMA: ';';
