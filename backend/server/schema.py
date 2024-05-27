from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from .serializers import ServerSerializer, ChannelSerializer

server_list_docs = extend_schema(
    responses=ServerSerializer(many=True),
    parameters=[
        OpenApiParameter(
            name='category',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description='Category of servers to retrieve',
        ),
        OpenApiParameter(
            name='qty',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description='Number of servers to retrieve',
        ),
        OpenApiParameter(
            name='by_user',
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            description='Filter servers by authenticated user (true/false)',
        ),
        OpenApiParameter(
            name='by_serverid',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description='Include server by server ID',
        ),
        OpenApiParameter(
            name='with_num_members',
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            description='Include the number of members for each server in the response',
        ),
    ]
)
