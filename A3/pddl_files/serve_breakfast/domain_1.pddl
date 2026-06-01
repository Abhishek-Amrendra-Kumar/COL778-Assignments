(define (domain serveBreakfast)
  (:requirements :strips :conditional-effects  :equality)

  ;; ───── Constants ────
  ;; Fixed objects in the scene
  (:constants bread egg fridge knife plate pan mug toaster stoveburner coffeemachine dining_table counter_1 counter_2 counter_1_l counter_2_l dining_table_l fridge_l default_l)

    ;; ───── Predicate Definitions ─────
    (:predicates
      (at ?loc)                ; Robot is at a specific location
      (on ?obj ?surf)          ; Object is on a surface or device
      (at-location ?obj ?loc) ; e.g., (at-location fridge fridge_l)
      (in ?obj ?cont)          ; Object is inside a container (like the fridge)
      (holding ?obj)           ; Robot is holding an object
      (hand-empty)             ; Robot's hand is empty
      (is-sliced ?obj)         ; Object has been sliced
      (is-toasted ?obj)        ; Object has been toasted
      (is-broken ?obj)
      (is-cooked ?obj)
      (is-filled ?obj)
      (is-on ?device)          ; Device is currently turned on
      (opened ?obj)            ; Container (like the fridge) is open
    )

    ;; ───── Action Definitions ─────
    ;; Move the robot between locations
    (:action move
      :parameters (?from ?to)
      :precondition (and (at ?from))
      :effect (and (not (at ?from)) (at ?to))
    )

    ;; Open a container
    (:action open
      :parameters (?obj ?loc)
      :precondition (and (at ?loc) (at-location ?obj ?loc) (not (opened ?obj)))
      :effect (opened ?obj)
    )

    ;; Pick up an object
    (:action pick
      :parameters (?obj ?container ?loc)
      :precondition (and (at ?loc) (hand-empty) (at-location ?container ?loc) (at-location ?obj ?loc)
                      (or (and (in ?obj ?container) (opened ?container)) (on ?obj ?container))
                      (or (not (= ?obj egg)) (not (is-broken ?obj)))
                    )
      :effect (and (holding ?obj) (not (hand-empty)) (not (at-location ?obj ?loc))
                   (not (in ?obj ?container)) (not (on ?obj ?container)))
    )

    ;; Put down an object
    (:action put
      :parameters (?obj ?container ?loc)
      :precondition (
        and 
        (at ?loc)
        (at-location ?container ?loc) 
        (holding ?obj) 

        (not (= ?container knife)) 
        (not (= ?container egg))
        (not (= ?container bread)) 
        (not (= ?container mug))

        (not (and (= ?obj egg) (= ?container pan) (is-broken ?obj)))
        (not (and (= ?obj egg) (= ?container stoveburner)))

        (or (not (= ?container toaster)) (is-sliced ?obj))
        (or (not (= ?container pan)) (= ?obj egg))
        (or (not (= ?container coffeemachine)) (= ?obj mug))

        (not (and (= ?obj pan) (= ?container fridge)))
        )
      :effect (and (not (holding ?obj)) (hand-empty) (on ?obj ?container) (at-location ?obj ?loc))
    )

    (:action slice
      :parameters (?obj ?loc)
      :precondition (
        and (at ?loc)
        (holding knife) 
        (at-location ?obj ?loc)
        (or (and (= ?obj bread) (on ?obj counter_1))
            (and (= ?obj egg) (on ?obj pan)))
        (exists (?s) (and (on ?obj ?s) (at-location ?s ?loc)))
        (not (is-broken ?obj))
      )
      :effect (and 
          ;; If it's bread, it becomes sliced
          (when (= ?obj bread) (is-sliced bread))
          ;; If it's the egg, it becomes broken
          (when (= ?obj egg) (is-broken egg))
      )
    )

    ;; Turn on a device (to toast the bread)
    (:action turn_on
      :parameters (?device ?loc)
      :precondition (
        and (at ?loc) 
        (at-location ?device ?loc) 
        (not (is-on ?device)) 
        (or (and (= ?device toaster) (on bread toaster))
            (and (= ?device stoveburner) (on pan stoveburner) (on egg pan) (is-broken egg))
            (and (= ?device coffeemachine) (on mug coffeemachine)))
        )
      :effect (
        and (is-on ?device)
        (when (and (= ?device stoveburner) (on pan stoveburner) (on egg pan) (is-broken egg)) (is-cooked egg))
        (when (= ?device toaster) (is-toasted bread))
        (when (and (= ?device coffeemachine) (on mug coffeemachine)) (is-filled mug))
        )
    )
    ;; Turn off a device
    (:action turn_off
      :parameters (?device ?loc)
      :precondition (
        and (at ?loc) 
        (at-location ?device ?loc) 
        (is-on ?device)
        )
      :effect (
        and (not (is-on ?device))
      )
    )
  )