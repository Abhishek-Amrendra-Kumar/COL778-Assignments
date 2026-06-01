
(define (problem serveBreakfast-totable)
(:domain serveBreakfast)
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
    (at-location egg fridge_l)
    (at-location pan counter_2_l)
    (at-location mug counter_2_l)
    (at-location stoveburner counter_2_l)
    (at-location coffeemachine counter_1_l)
    
    
    ;; Initial containment
    (in bread fridge)
    (in egg fridge)
    (on knife counter_1)
    (on pan counter_2)
    (on mug counter_2)
    (on plate dining_table)
    (on toaster counter_1)
    

  )

  (:goal 
   (and 
     (is-sliced bread) 
     (is-toasted bread)
     (on bread plate)
     (on plate dining_table)

     (on egg pan)  
     (on pan dining_table)        
     (is-cooked egg)
     
     (is-filled mug)
     (on mug dining_table)

    )
  )
)