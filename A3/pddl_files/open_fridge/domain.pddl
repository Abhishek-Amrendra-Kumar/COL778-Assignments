(define (domain openFridge)
  (:requirements :strips :conditional-effects  :equality)

  ;; ───── Constants ────
  ;; Fixed objects in the scene
  (:constants bread egg fridge knife plate pan mug toaster stoveburner coffeemachine dining_table counter_1 counter_2 counter_1_l counter_2_l dining_table_l fridge_l default_l)

    ;; ───── Predicate Definitions ─────
    (:predicates
      (open ?d)
      (robotat ?l)
    )

    (:action open
      :parameters (?d ?l)
      :precondition (and (robotat ?l) (not (open ?d)))
      :effect (open ?d)
    )
)