Mesh.CharacteristicLengthMin = 2;
Mesh.CharacteristicLengthMax = 4;


SetFactory ("OpenCASCADE");
Torus (1) = {0, 0, 0, 60, 30, 2*Pi};
Torus (2) = {0, 0, 0, 60, 18, 2*Pi};
BooleanDifference (8) = {Volume {1}; Delete; } {Volume {2}; Delete; };
