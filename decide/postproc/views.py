from rest_framework.views import APIView
from rest_framework.response import Response


class PostProcView(APIView):

    def identity(self, options):
        out = []

        for opt in options:
            out.append({
                **opt,
                'postproc': opt['votes'],
            });

        out.sort(key=lambda x: -x['postproc'])
        return Response(out)

    def dhondt(self, options):
        out = options.copy()
        aux = [0]*len(options)
        seats = 8
        i=0

        while i<seats:
            votes=-1
            for index, opt in enumerate(out):
                if(opt['votes']/(aux[index]+1)>votes):
                    votes = opt['votes']/(aux[index]+1)
                    best = index

            aux[best] = aux[best]+1
            i++
        
        for index, opt in enumerate(out):
            opt['seats'] = aux[index]

        return Response(out)

    def post(self, request):
        """
         * type: IDENTITY | EQUALITY | WEIGHT
         * options: [
            {
             option: str,
             number: int,
             votes: int,
             ...extraparams
            }
           ]
        """

        t = request.data.get('type', 'IDENTITY')
        opts = request.data.get('options', [])

        if t == 'IDENTITY':
            return self.identity(opts)

        else if t == 'DHONDT':
            return self.dhondt(opts)            

        return Response({})
