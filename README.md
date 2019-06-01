# Boids
An implementation of the Greg Reynolds' Boid system. _"Boids"_ is an artificial life program, which simulates the flocking behaviour of birds. The name "boid" corresponds to a shortened version of "bird-oid object" (or "bird like object"). Boids is an example of emergent behavior; that is, the complexity of Boids arises from the interaction of individual agents adhering to a set of rules. The rules are as follows:
- *Separation*: steer to avoid crowding local flockmates
- *Alignment*: steer towards the average heading of local flockmates
- *Cohesion*: steer to move towards the average position (center of mass) of local flockmates

In this implementation, a couple extra rules are used:
- *Speed limit*: defines a maximum velocity the boids can move at
- *Boundries*: defines an area that the boids tend to stay in so as to not let the boids travel too far out of the screen. This is not a strict boundry.
