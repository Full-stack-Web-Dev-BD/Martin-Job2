
using AutoMapper;
using log4net;
using Microsoft.Extensions.Configuration;
using Newtonsoft.Json;
using Newtonsoft.Json.Serialization;
using RocketSource.Models;
using System.Net.Http.Headers;
using System.Net.Http.Json;


namespace RocketSource
{
    public class RocketSourceService : IRocketSourceService
    {
        private readonly string _rsUrl;
        private readonly string _apiKey;
        private readonly string _usdToGbp;
        private readonly IMapper _mapper;
        private readonly List<string> _scanIds;
        private readonly string _scanDirectory;
        private readonly ILog _log4net;
        public RocketSourceService(IConfigurationRoot config, IMapper mapper)
        {
            //var _mapperConfig = new MapperConfiguration(map => map.AddProfile<MapperProfile>());
            //_mapper = _mapperConfig.CreateMapper();
            _mapper = mapper;
            _rsUrl = config["RS:BaseUrl"];
            _apiKey = config["RS:ApiKey"];
            _scanIds = config["RS:ScanIds"].Split(",").ToList();
            _usdToGbp = config["Units:USDtoGBP"];
            _scanDirectory = $"{config["RS:OutputDirectory"]}";
            _log4net = LogManager.GetLogger(typeof(Program));
        }

        public void ProcessScans()
        {

            Directory.CreateDirectory(_scanDirectory);
            foreach (var scanId in _scanIds) {
                Console.WriteLine($"Processing Scan {scanId}");
                try
                {
                    GetScanResult(int.Parse(scanId));
                }
                catch (Exception ex)
                {
                    _log4net.Error($"Error while getting scan results for scan {scanId}", ex);
                }
            }
        }

        public void GetScanResult(int scanId)
        {
            try
            {

                var pageNumber = 1;
                List<USScanData> finalScanResults = new List<USScanData>();
                using HttpClient client = new();
                client.BaseAddress = new Uri(_rsUrl);
                client.DefaultRequestHeaders.Accept.Clear();
                client.DefaultRequestHeaders.Accept.Add(
                    new MediaTypeWithQualityHeaderValue("application/json"));
                client.DefaultRequestHeaders.Authorization =
                        new AuthenticationHeaderValue("Bearer", _apiKey);
                var emptyResponse = false;
                var attempt = 1;
                do
                {
                    _log4net.Info($"processing page : {pageNumber}");
                    var reqBody = new
                    {
                        per_page = 100,
                        page = pageNumber
                    };

                    try
                    {
                        var rsResponse = client.PostAsJsonAsync($"api/v3/scans/{scanId}", reqBody).Result;
                        if (rsResponse.IsSuccessStatusCode)
                        {
                            var resContent = rsResponse.Content.ReadAsStringAsync().Result;//JsonConvert.DeserializeObject<List<RestResponse>>(response.Content.ReadAsStringAsync().Result);//
                            var scanResults = JsonConvert.DeserializeObject<RocketSourceScanResult>(resContent);
                            var scans = _mapper.Map<List<USScanData>>(scanResults?.Data);
                            finalScanResults.AddRange(scans);
                            emptyResponse = scanResults?.Data.Count == 0;
                            pageNumber++;
                            attempt = 1;
                        }
                        else
                        {
                            attempt++;
                            _log4net.Warn($"Error while getting results for scan {scanId} : {rsResponse.Content}");
                            Thread.Sleep(5000);
                        }
                    }
                    catch (Exception ex)
                    {
                        attempt++;
                        _log4net.Warn($"Error while getting results for scan {scanId}", ex);
                        Thread.Sleep(5000);
                    }
                    
                } while (!emptyResponse && attempt <= 3);

                string fileName = $"{_scanDirectory}/ScanResults_{scanId}_{DateTime.Now.ToString("ddMMyyThhmmss")}.json";
                _log4net.Info($"Generating file for Scan {scanId}");
                using (StreamWriter file = File.CreateText(fileName))
                {
                    DefaultContractResolver contractResolver = new DefaultContractResolver
                    {
                        NamingStrategy = new SnakeCaseNamingStrategy()
                    };
                    JsonSerializer serializer = new JsonSerializer();
                    serializer.ContractResolver = contractResolver;
                    //serialize object directly into file stream
                    serializer.Serialize(file, finalScanResults);
                }
                _log4net.Info($"Generated file for Scan {scanId} : {fileName}");
            }
            catch (Exception ex)
            {
                _log4net.Error($"Error while getting results for scan {scanId}", ex);
                throw;
            }

        }
    }
}
