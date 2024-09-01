-- Strip Mining Script
-- Set the tunnel length (how far forward the turtle will dig)
local length = 50  -- Change this to the desired length

-- Function to dig forward and ensure the path is clear
function digForward()
  while turtle.detect() do
    turtle.dig()
  end
  turtle.forward()
end

-- Function to dig upwards
function digUp()
  while turtle.detectUp() do
    turtle.digUp()
  end
end

-- Function to dig downwards
function digDown()
  while turtle.detectDown() do
    turtle.digDown()
  end
end

-- Main strip mining function
function mineTunnel()
  for i = 1, length do
    digForward()  -- Move forward and dig
    digUp()       -- Dig above
    digDown()     -- Dig below
  end
end

-- Return to the starting position
function returnToStart()
  turtle.turnLeft()
  turtle.turnLeft()
  for i = 1, length do
    turtle.forward()
  end
  turtle.turnLeft()
  turtle.turnLeft()
end

-- Main program execution
mineTunnel()
returnToStart()
print("Mining complete. Turtle has returned to the start.")
