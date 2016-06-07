(declare-datatypes () ((Content Apples Oranges Mixes))) ; Scalas
(declare-const realApple Content)
(declare-const realOrange Content)
(declare-const realMixed Content)
(assert (distinct realApple realOrange realMixed))  ; contents of each crates are all distinct
(assert (not (= realApple Apples))) 
(assert (not (= realOrange Oranges)))
(assert (not (= realMixed Mixes)))  ; all the labels have been shuffled

(assert (or (= realMixed Apples) (= realMixed Mixes))); pick an apple from the mixed crate
(check-sat)
(get-model)
