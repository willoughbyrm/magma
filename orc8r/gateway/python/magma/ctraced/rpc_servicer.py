"""
Copyright 2020 The Magma Authors.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from orc8r.protos.ctraced_pb2_grpc import CallTraceServiceServicer,\
    add_CallTraceServiceServicer_to_server
from orc8r.protos.ctraced_pb2 import StartTraceRequest, StartTraceResponse,\
    EndTraceRequest, EndTraceResponse
from .trace_manager import TraceManager


class CtraceDRpcServicer(CallTraceServiceServicer):
    """
    gRPC based server for CtraceD.
    """

    def __init__(self, trace_manager: TraceManager):
        self._trace_mgr = trace_manager
        pass

    def add_to_server(self, server):
        """
        Add the servicer to a gRPC server
        """
        add_CallTraceServiceServicer_to_server(self, server)

    def StartCallTrace(
        self,
        request: StartTraceRequest,
        _context,
    ) -> StartTraceResponse:
        success = self._trace_mgr.start_trace(
            request.trace_id,
            request.timeout,
            request.capture_filters,
            request.display_filters,
        )
        response = StartTraceResponse(success=success)
        return response

    def EndCallTrace(
        self,
        _request: EndTraceRequest,
        _context,
    ) -> EndTraceResponse:
        res = self._trace_mgr.end_trace() # type: EndTraceResult
        response = EndTraceResponse(
            success=True,
            trace_content=res.data,
        )
        return response
