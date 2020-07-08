# 3D Processing Techniques
## Point, Plane, Distances
s,t,a,b,c : scalars
p,q,p0,q0 : absolute coorinate points
U,V,W,N   : vectors

### Point-Plane Distance
Plane = (p0, N)
Point out of plane: p

Distance between generic point p and plane point p0
1) `V = (p-p0)`

Projection of V onto plane normal vector (can be longer than unit-vector). Output is a vector V_II parallel to V,
2) `V_II = dot(V, N)*N`

Orthogonal vector V_T, the distance between projection point q0 and p0, is the same as orthogonal vector component of V,
3) `V_T = V - V_II`

The final point q0 projected on to the plane is:
`q0 = p0 - V_T`

or 

`q0 = p - V_II`


