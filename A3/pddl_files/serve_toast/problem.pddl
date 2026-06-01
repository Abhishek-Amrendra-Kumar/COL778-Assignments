
(define (problem serveToast-totable)
  (:domain serveToast)

  (:init
    (at default_l)
    (hand-empty)

    ;; Define which surfaces are at which locations
    (at-location fridge fridge_l)
    (at-location counter_1 counter_1_l)
    (at-location counter_2 counter_2_l)
    (at-location toaster counter_1_l)
    (at-location knife counter_1_l)
    (at-location dining_table dining_table_l)
    (at-location plate dining_table_l)
    (at-location bread fridge_l)
    
    
    ;; Initial containment
    (in bread fridge)

    (on knife counter_1)
    
    (on toaster counter_1)

    (on plate dining_table)
  )

  (:goal
   (and 
    (on knife counter_1) 
    (is-toasted bread)
    (hand-empty)
    (on bread plate)
    (at-location bread dining_table_l) 
    (opened fridge) 
    (at dining_table_l) 
    (is-sliced bread) 
    (at-location knife counter_1_l) 

   )
  )
)