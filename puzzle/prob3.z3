(declare-datatypes () ((Content Apples Oranges Mixes))) ; Scalas
(declare-const realApple Content)
(declare-const realOrange Content)
(declare-const realMixed Content)
(assert (distinct realApple realOrange realMixed))  ; contents of each crates are all distinct
(assert (not (= realApple Apples))) 
(assert (not (= realOrange Oranges)))
(assert (not (= realMixed Mixes)))  ; all the labels have been shuffled

(assert (or (= realOrange Apples) (= realOrange Mixes))); pick an apple from the "orange" crate
(check-sat)
(get-model)

(assert (not (and (and
  (= realApple Oranges)
  (= realMixed Apples))
  (= realOrange Mixes))
))
(check-sat)
(get-model)
