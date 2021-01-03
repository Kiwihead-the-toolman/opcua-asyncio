import asyncio
import logging

from asyncua import Client

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger('asyncua')


class SubHandler(object):
    """
    Subscription Handler. To receive events from server for a subscription
    data_change and event methods are called directly from receiving thread.
    Do not do expensive, slow or network operation there. Create another
    thread if you need to do such a thing
    """
    def datachange_notification(self, node, val, data):
        print("New data change event", node, val)

    def event_notification(self, event):
        print("New event", event)


async def main():
    print("")
    print("Start of url")
    print("")
    url = "opc.tcp://localhost:4840/freeopcua/server/"
    async with Client(url=url) as client:
        print("")
        print("Start of client")
        print("")
        _logger.info("Root node is: %r", client.nodes.root)
        _logger.info("Objects node is: %r", client.nodes.objects)
        
        # Node objects have methods to read and write node attributes as well as browse or populate address space
        _logger.info("Children of root are: %r", await client.nodes.root.get_children())
        print("")
        print("End of client")
        print("")
        print("")
        print("Start of uri")
        print("")
        uri = "http://examples.freeopcua.github.io"
        idx = await client.get_namespace_index(uri)
        _logger.info("index of our namespace is %s", idx)
        print("")
        print("End of uri")
        print("")
        # get a specific node knowing its node id
        # var = client.get_node(ua.NodeId(1002, 2))
        #var = client.get_node("ns=3;i=2002")
        #print(var)
        #await var.read_data_value() # get value of node as a DataValue object
        #await var.read_value() # get value of node as a python builtin
        #await var.write_value(ua.Variant([23], ua.VariantType.Int64)) #set node value using explicit data type
        #await var.write_value(3.9) # set node value using implicit data type

        # Now getting a variable node using its browse path
        print("")
        print("Start of browse path")
        print("")
        myvar = await client.nodes.root.get_child(["0:Objects", "2:MyObject", "2:MyVariable"])
        obj = await client.nodes.root.get_child(["0:Objects", "2:MyObject"])
        _logger.info("myvar is: %r", myvar)
        print("")
        print("End of browse path")
        print("")

        # subscribing to a variable node
        print("")
        print("Start of subscription")
        print("")
        handler = SubHandler()
        sub = await client.create_subscription(500, handler)
        handle = await sub.subscribe_data_change(myvar)
        await asyncio.sleep(5.0)
        print("")
        print("End of subscription")
        print("")
        # we can also subscribe to events from server
        print("")
        print("Start of events")
        print("")
        await sub.subscribe_events()
        print("")
        print("End of events")
        print("")
        print("")
        print("Start of unsubscribe")
        print("")
        await sub.unsubscribe(handle)
        print("")
        print("End of unsubscribe")
        print("")
        print("")
        print("Start of delete")
        print("")
        await sub.delete()
        print("")
        print("End of delete")
        print("")

        # calling a method on server
        print("")
        print("Start of method")
        print("")
        res = await obj.call_method("2:multiply", 3, "klk")
        _logger.info("method result is: %r", res)
        print("")
        print("End of method")
        print("")


if __name__ == "__main__":
    asyncio.run(main())
