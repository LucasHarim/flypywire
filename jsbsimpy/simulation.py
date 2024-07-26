from typing import List, Dict, Union
import jsbsim
from jsbsimpy.fdm_pubsub import FDMPublisher
from py_trees.trees import BehaviourTree
import jsbsimpy.properties as prp

class SimSession:

    def __init__(self,
        jsbsim_root_dir: str,
        aircraft_model: str,
        ic_path: str = "",
        sim_dt: float = 0.03,
        realtime: bool = True) -> None:

        self.fdm = jsbsim.FGFDMExec(root_dir = jsbsim_root_dir)
        self.jsbsim_root_dir = jsbsim_root_dir
        self.aircraft_model = aircraft_model
        self.ic_path = ic_path
        self.sim_dt = sim_dt
        self.realtime = realtime
        self.IC_properties = dict()

        self.fdm_publisher: FDMPublisher = None
        self.properties_to_publish: List[prp.Property | prp.BoundedProperty] = list()
        self.bt: BehaviourTree = None
        
        
    
    def init(self) -> None:
        
        self.fdm.load_model(self.aircraft_model)
        if len(self.ic_path) > 0: self.fdm.load_ic(self.ic_path, False)

        self.fdm.set_dt(self.sim_dt)
        [self.fdm.set_property_value(prop.name, self.IC_properties[prop])\
            for prop in self.IC_properties]
        
        _success = self.fdm.run_ic()
        if not _success:
            raise Exception("Initial Condition (IC) did not run as expected.")
        
    
    def set_IC_properties(self, properties: Dict[Union[prp.Property, prp.BoundedProperty], float]) -> None:
        self.IC_properties = properties
        
    @property
    def _publish_fdm_outputs(self) -> bool:

        return isinstance(self.fdm_publisher, FDMPublisher)
    
    @property
    def _tick_bt(self) -> bool:

        return isinstance(self.bt, BehaviourTree)
    

    def add_fdm_publisher(self,
        fdm_pub: FDMPublisher,
        properties_to_publish: List[prp.Property | prp.BoundedProperty]) -> None:
        
        if not isinstance(fdm_pub, FDMPublisher): 
            raise TypeError("fdm_pub must be of type FDMPublisher")
        
        self.fdm_publisher = fdm_pub
        self.properties_to_publish = properties_to_publish
    

    def add_behaviour_tree(self, bt: BehaviourTree) -> None:

        if not isinstance(bt, BehaviourTree): 
            raise TypeError("bt argument must be of type BehaviourTree")
        
        self.bt = bt


    def run_step(self) -> None:

        self.fdm.run()
        
        if self._tick_bt: self.bt.tick()
        
        if self._publish_fdm_outputs:

            self.fdm_publisher.publish_fdm_outputs(
                fdm_outputs = prp.get_outputs_from_fdm(
                    self.fdm,
                    self.properties_to_publish),
                realtime = self.realtime)
    

        
        